import json
from pprint import pformat, pprint
import requests
from src.datatypes import StrategyData
from typing import List, TypedDict, Any
import dataclasses


class RAGInsertData(TypedDict):
    """
    Type definition for data to be inserted into the RAG system.
    
    Attributes:
        strategy_id (str): Unique identifier for the strategy
        summarized_desc (str): Summarized description of the strategy
    """
    strategy_id: str
    summarized_desc: str


class Metadata(TypedDict):
    """
    Type definition for metadata associated with RAG content.
    
    Attributes:
        created_at (str): Timestamp when the content was created
        reference_id (str): Reference identifier for the content
        strategy_data (str): JSON string containing StrategyData
    """
    created_at: str
    reference_id: str
    strategy_data: str  # JSON string containing StrategyData


class PageContent(TypedDict):
    """
    Type definition for a page of content in the RAG system.
    
    Attributes:
        metadata (Metadata): Metadata associated with the content
        page_content (str): The actual content text
    """
    metadata: Metadata
    page_content: str


class StrategyResponse(TypedDict):
    """
    Type definition for the response from the RAG API when retrieving strategies.
    
    Attributes:
        data (List[PageContent]): List of page content items
        msg (str): Message from the API
        status (str): Status of the response
    """
    data: List[PageContent]
    msg: str
    status: str


class RAGClient:
    """
    Client for interacting with the Retrieval-Augmented Generation (RAG) API.
    
    This class provides methods to save strategy data to the RAG system and
    retrieve relevant strategies based on a query.
    """
    def __init__(
        self,
        agent_id: str,
        session_id: str,
        base_url: str = "http://localhost:8080",
    ):
        """
        Initialize the RAG client with agent and session information.
        
        Args:
            agent_id (str): Identifier for the agent
            session_id (str): Identifier for the session
            base_url (str, optional): Base URL for the RAG API. 
                Defaults to "localhost:8080".
        """
        self.base_url = base_url
        self.agent_id = agent_id
        self.session_id = session_id

    def save_result_batch(self, batch_data: List[StrategyData]) -> Any:
        """
        Save a batch of strategy data to the RAG system.
        
        This method sends multiple strategy data items to the RAG API in a single request.
        
        Args:
            batch_data (List[StrategyData]): List of strategy data to save
            
        Returns:
            Any: Response from the API
            
        Raises:
            requests.HTTPError: If the API request fails
        """
        if not batch_data:
            print("No batch data to save")
            return {}
            
        try:
            url = f"{self.base_url}/save_result_batch"

            payload = []

            for data in batch_data:
                payload.append(
                    {
                        "strategy": data.summarized_desc,
                        "strategy_data": json.dumps(dataclasses.asdict(data)),
                        "reference_id": data.strategy_id,
                        "agent_id": self.agent_id,
                        "session_id": self.session_id,
                    }
                )

            response = requests.post(url, json=payload, timeout=5)
            response.raise_for_status()

            r = response.json()

            return r
        except Exception as e:
            print(f"Warning: Failed to save result batch to RAG: {e}")
            return {}

    def relevant_strategy_raw(self, query: str) -> List[StrategyData]:
        """
        Retrieve strategies relevant to the given query.
        
        This method searches the RAG system for strategies that are semantically
        similar to the provided query.
        
        Args:
            query (str): The search query
            
        Returns:
            List[StrategyData]: List of relevant strategies
            
        Raises:
            requests.HTTPError: If the API request fails
        """
        try:
            url = f"{self.base_url}/relevant_strategy"

            payload = {
                "query": query,
                "agent_id": self.agent_id,
                "session_id": self.session_id,
            }

            response = requests.post(url, json=payload, timeout=5)
            response.raise_for_status()

            r: StrategyResponse = response.json()

            result = []
            for item in r["data"]:
                strategy_data = json.loads(item["metadata"]["strategy_data"])
                result.append(
                    StrategyData(
                        strategy_id=strategy_data["strategy_id"],
                        agent_id=strategy_data["agent_id"],
                        parameters=strategy_data["parameters"],
                        summarized_desc=strategy_data["summarized_desc"],
                        full_desc=strategy_data["full_desc"],
                    )
                )

            return result
        except Exception as e:
            print(f"Warning: Failed to get relevant strategies from RAG: {e}")
            return []
