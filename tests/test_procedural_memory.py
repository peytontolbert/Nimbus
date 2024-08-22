import unittest
from memory.procedural_memory import ProceduralMemory, ToolNotFoundException
from workspace.tools.base import AgentTool
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain_community.vectorstores import FAISS

class TestProceduralMemory(unittest.TestCase):
    def setUp(self):
        self.tools = [
            AgentTool(name='Tool1', description='Description1'),
            AgentTool(name='Tool2', description='Description2')
        ]
        self.embeddings = OpenAIEmbeddings()
        self.docs = [
            Document(page_content=tool.description, metadata={"index": i})
            for i, tool in enumerate(self.tools)
        ]
        self.vector_store = FAISS.from_documents(self.docs, self.embeddings)
        self.memory = ProceduralMemory(tools=self.tools, embeddings=self.embeddings, docs=self.docs, vector_store=self.vector_store)

    def test_memorize_tools(self):
        new_tools = [
            AgentTool(name='Tool3', description='Description3'),
            AgentTool(name='Tool4', description='Description4')
        ]
        self.memory.memorize_tools(new_tools)
        self.assertEqual(len(self.memory.tools), 4)

    def test_remember_tool_by_name(self):
        tool = self.memory.remember_tool_by_name('Tool1')
        self.assertEqual(tool.name, 'Tool1')
        self.assertEqual(tool.description, 'Description1')
        with self.assertRaises(ToolNotFoundException):
            self.memory.remember_tool_by_name('NonExistentTool')

    def test_remember_relevant_tools(self):
        relevant_tools = self.memory.remember_relevant_tools('Description1')
        self.assertEqual(len(relevant_tools), 1)
        self.assertEqual(relevant_tools[0].name, 'Tool1')

    def test_remember_all_tools(self):
        all_tools = self.memory.remember_all_tools()
        self.assertEqual(len(all_tools), 2)

if __name__ == '__main__':
    unittest.main()
