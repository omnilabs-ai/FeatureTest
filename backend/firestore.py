from firebase_admin import firestore
from typing import Dict, List, Optional, Any

class FirestoreDB:
    def __init__(self):
        self.db = firestore.client()

    def _get_user_collection(self, user_id: str, collection_name: str) -> firestore.CollectionReference:
        """
        Get a reference to a user-specific collection
        """
        return self.db.collection('users').document(user_id).collection(collection_name)

    async def create_document(self, user_id: str, collection_name: str, data: Dict[str, Any]) -> str:
        """
        Create a new document in a user's collection
        
        Args:
            user_id: The ID of the authenticated user
            collection_name: The name of the collection
            data: The document data to store
            
        Returns:
            The ID of the created document
        """
        collection_ref = self._get_user_collection(user_id, collection_name)
        doc_ref = collection_ref.document()
        await doc_ref.set(data)
        return doc_ref.id

    async def get_document(self, user_id: str, collection_name: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific document from a user's collection
        
        Returns:
            The document data or None if not found
        """
        doc_ref = self._get_user_collection(user_id, collection_name).document(doc_id)
        doc = await doc_ref.get()
        return doc.to_dict() if doc.exists else None

    async def get_all_documents(self, user_id: str, collection_name: str) -> List[Dict[str, Any]]:
        """
        Retrieve all documents from a user's collection
        """
        collection_ref = self._get_user_collection(user_id, collection_name)
        docs = await collection_ref.get()
        return [doc.to_dict() for doc in docs]

    async def update_document(self, user_id: str, collection_name: str, doc_id: str, data: Dict[str, Any]) -> bool:
        """
        Update a specific document in a user's collection
        
        Returns:
            True if update was successful, False if document not found
        """
        doc_ref = self._get_user_collection(user_id, collection_name).document(doc_id)
        doc = await doc_ref.get()
        if not doc.exists:
            return False
        
        await doc_ref.update(data)
        return True

    async def delete_document(self, user_id: str, collection_name: str, doc_id: str) -> bool:
        """
        Delete a specific document from a user's collection
        
        Returns:
            True if deletion was successful, False if document not found
        """
        doc_ref = self._get_user_collection(user_id, collection_name).document(doc_id)
        doc = await doc_ref.get()
        if not doc.exists:
            return False
        
        await doc_ref.delete()
        return True

    async def query_documents(self, 
                            user_id: str, 
                            collection_name: str, 
                            field: str, 
                            operator: str, 
                            value: Any) -> List[Dict[str, Any]]:
        """
        Query documents in a user's collection based on a field condition
        
        Args:
            user_id: The ID of the authenticated user
            collection_name: The name of the collection
            field: The field to query on
            operator: The comparison operator ('==', '>', '<', '>=', '<=', '!=')
            value: The value to compare against
            
        Returns:
            List of documents matching the query
        """
        collection_ref = self._get_user_collection(user_id, collection_name)
        query = collection_ref.where(field, operator, value)
        docs = await query.get()
        return [doc.to_dict() for doc in docs]
