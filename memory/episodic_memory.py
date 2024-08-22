from typing import List, Dict, Any, Optional
from langchain_community.vectorstores import VectorStore, FAISS
from langchain_openai import OpenAIEmbeddings
from prompts.summarize.prompt import get_template
import openai
import time


class Episode:
    def __init__(self, thoughts: Dict[str, Any], action: Dict[str, Any], result: Optional[str] = None, summary: Optional[str] = None) -> None:
        self.thoughts = thoughts
        self.action = action
        self.result = result
        self.summary = summary


class EpisodicMemory:
    def __init__(self, num_episodes: int = 0, store: Dict[str, Episode] = {}, embeddings: Optional[OpenAIEmbeddings] = None, vector_store: Optional[VectorStore] = None) -> None:
        self.num_episodes = num_episodes
        self.store = store
        self.embeddings = embeddings if embeddings is not None else OpenAIEmbeddings()
        self.vector_store = vector_store

    def memorize_episode(self, episode: Episode) -> None:
        self.num_episodes += 1
        self.store[str(self.num_episodes)] = episode
        self._embed_episode(episode)

    def summarize_and_memorize_episode(self, episode: Episode) -> str:
        summary = self._summarize(episode.thoughts, episode.action, episode.result)
        episode.summary = summary
        self.memorize_episode(episode)
        return summary

    def _summarize(self, thoughts: Dict[str, Any], action: Dict[str, Any], result: str) -> str:
        prompt = get_template()
        BASE_TEMPLATE = """
        [THOUGHTS]
        {thoughts}

        [ACTION]
        {action}

        [RESULT OF ACTION]
        {result}

        [INSTRUSCTION]
        Using above [THOUGHTS], [ACTION], and [RESULT OF ACTION], please summarize the event.

        [SUMMARY]
        """
        chat_input = BASE_TEMPLATE.format(thoughts=thoughts, action=action, result=result)
        retries = 15
        delay = 5
        for i in range(retries):
            try:
                results = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k",
                    messages=[{"role": "system", "content": chat_input}],
                )
                result = str(results["choices"][0]["message"]["content"])
            except openai.error.ServiceUnavailableError:
                if i < retries - 1:
                    time.sleep(delay)
                else:
                    raise
        return result

    def remember_all_episode(self) -> List[Episode]:
        return self.store

    def remember_recent_episodes(self, n: int = 5) -> List[Episode]:
        if not self.store:
            return self.store
        n = min(n, len(self.store))
        return list(self.store.values())[-n:]

    def remember_last_episode(self) -> Episode:
        if not self.store:
            return None
        return self.store[-1]

    def remember_related_episodes(self, query: str, k: int = 5) -> List[Episode]:
        if self.vector_store is None:
            return []
        if query is not None:
            relevant_documents = self.vector_store.similarity_search(query, k=k)
            result = []
            for d in relevant_documents:
                episode = Episode(
                    thoughts=d.metadata["thoughts"],
                    action=d.metadata["action"],
                    result=d.metadata["result"],
                    summary=d.metadata["summary"],
                )
                result.append(episode)
            return result

    def _embed_episode(self, episode: Episode) -> None:
        texts = [episode.summary]
        metadatas = [
            {
                "index": self.num_episodes,
                "thoughts": episode.thoughts,
                "action": episode.action,
                "result": episode.result,
                "summary": episode.summary,
            }
        ]
        if self.vector_store is None:
            self.vector_store = FAISS.from_texts(
                texts=texts, embedding=self.embeddings, metadatas=metadatas
            )
        else:
            self.vector_store.add_texts(texts=texts, metadatas=metadatas)

    def save_local(self, path: str) -> None:
        if self.vector_store is not None:
            self.vector_store.save_local(folder_path=path)

    def load_local(self, path: str) -> None:
        self.vector_store = FAISS.load_local(
            folder_path=path, embeddings=self.embeddings
        )

