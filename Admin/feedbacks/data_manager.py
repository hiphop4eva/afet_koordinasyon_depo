from datetime import datetime
from database import get_firestore

class FeedbackDataManager:
    def __init__(self):
        self.db = get_firestore()
        self.feedbacks_ref = self.db.collection('feedbacks')

    def get_all_feedbacks(self):
        """Tüm geri bildirimleri getir"""
        feedbacks = []
        docs = self.feedbacks_ref.stream()
        
        for doc in docs:
            feedback_data = doc.to_dict()
            feedback_data['id'] = doc.id
            feedbacks.append(feedback_data)
            
        return feedbacks

    def update_feedback_status(self, feedback_id, new_status):
        """Geri bildirim durumunu güncelle"""
        self.feedbacks_ref.document(feedback_id).update({
            'status': new_status,
            'lastUpdated': datetime.now()
        })

    def add_reply(self, feedback_id, reply_content, sender="Admin"):
        """Geri bildirime yanıt ekle"""
        reply_data = {
            'content': reply_content,
            'sender': sender,
            'timestamp': datetime.now(),
        }
        
        # Yanıtı alt koleksiyona ekle
        self.feedbacks_ref.document(feedback_id).collection('replies').add(reply_data)
        
        # Ana dokümanın durumunu güncelle
        self.update_feedback_status(feedback_id, "Okundu")

    def get_feedback_replies(self, feedback_id):
        """Bir geri bildirimin tüm yanıtlarını getir"""
        replies = []
        reply_docs = self.feedbacks_ref.document(feedback_id).collection('replies').order_by('timestamp').stream()
        
        for doc in reply_docs:
            reply_data = doc.to_dict()
            reply_data['id'] = doc.id
            replies.append(reply_data)
            
        return replies 