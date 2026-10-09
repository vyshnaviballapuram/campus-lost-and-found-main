"""
AI Matching Module for Smart Item Matching.
Yeh module TF-IDF aur Cosine Similarity use karta hai items match karne ke liye.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def get_similar_items(current_item, all_items, top_n=5):
    """
    Current item ke similar items dhundh kar return karta hai.
    TF-IDF vectorization aur cosine similarity use karta hai.
    
    Parameters:
    -----------
    current_item : Item
        Wo item jis ke liye matches dhundne hain
    all_items : QuerySet
        Sab items jismein se matches dhundne hain
    top_n : int
        Kitne top matches return karne hain (default 5)
    
    Returns:
    --------
    list : Top matching items ki list with similarity scores
    """
    
    # Agar items kam hain to empty list return karo
    if len(all_items) == 0:
        return []
    
    # Current item ki description prepare karna
    current_text = prepare_item_text(current_item)
    
    # Sab items ki descriptions prepare karna
    all_texts = [prepare_item_text(item) for item in all_items]
    
    # Current item bhi add karna comparison ke liye
    all_texts.insert(0, current_text)
    
    # TF-IDF Vectorizer initialize karna
    # Yeh text ko numerical vectors mein convert karta hai
    vectorizer = TfidfVectorizer(
        stop_words='english',      # Common English words ignore karna
        ngram_range=(1, 2),        # Unigrams aur bigrams use karna
        max_features=5000,         # Maximum features limit
        lowercase=True,            # Sab lowercase mein convert
    )
    
    try:
        # Sab texts ko TF-IDF vectors mein convert karna
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        
        # Cosine similarity calculate karna
        # Pehla vector (index 0) current item ka hai
        cosine_similarities = cosine_similarity(
            tfidf_matrix[0:1],  # Current item ka vector
            tfidf_matrix[1:]     # Baaki sab items ke vectors
        ).flatten()
        
        # Top N similar items ke indices dhundna
        similar_indices = np.argsort(cosine_similarities)[::-1][:top_n]
        
        # Results prepare karna with similarity scores
        results = []
        for idx in similar_indices:
            if cosine_similarities[idx] > 0:  # Sirf positive similarity wale
                results.append({
                    'item': all_items[idx],
                    'similarity_score': round(cosine_similarities[idx] * 100, 2)
                })
        
        return results
        
    except Exception as e:
        # Agar koi error aaye to empty list return karo
        print(f"Error in AI matching: {e}")
        return []


def prepare_item_text(item):
    """
    Item ko text format mein prepare karta hai AI matching ke liye.
    Title, description, category aur location combine karta hai.
    
    Parameters:
    -----------
    item : Item
        Item object jisko text mein convert karna hai
    
    Returns:
    --------
    str : Combined text string for TF-IDF processing
    """
    
    # Sab relevant fields combine karna
    text_parts = [
        item.title or '',
        item.description or '',
        item.get_category_display() if hasattr(item, 'get_category_display') else '',
        item.location or '',
    ]
    
    # Sab parts ko space se join karna
    combined_text = ' '.join(text_parts)
    
    # Extra whitespace remove karna
    combined_text = ' '.join(combined_text.split())
    
    return combined_text


def find_matches_for_lost_item(lost_item, found_items_queryset, threshold=10, top_n=5):
    """
    Lost item ke liye potential found item matches dhundta hai.
    Sirf wo matches return karta hai jo threshold se upar hain.
    
    Parameters:
    -----------
    lost_item : Item
        Lost item jis ke liye matches dhundne hain
    found_items_queryset : QuerySet
        Found items ka queryset
    threshold : float
        Minimum similarity percentage (default 10%)
    top_n : int
        Maximum matches return karne hain (default 5)
    
    Returns:
    --------
    list : Matching found items with similarity scores
    """
    
    # QuerySet ko list mein convert karna
    found_items = list(found_items_queryset)
    
    # Similar items dhundna
    matches = get_similar_items(lost_item, found_items, top_n=top_n)
    
    # Threshold se filter karna
    filtered_matches = [
        match for match in matches 
        if match['similarity_score'] >= threshold
    ]
    
    return filtered_matches


def find_matches_for_found_item(found_item, lost_items_queryset, threshold=10, top_n=5):
    """
    Found item ke liye potential lost item matches dhundta hai.
    Yeh function tab use hota hai jab koi found item post kare.
    
    Parameters:
    -----------
    found_item : Item
        Found item jis ke liye matches dhundne hain
    lost_items_queryset : QuerySet
        Lost items ka queryset
    threshold : float
        Minimum similarity percentage (default 10%)
    top_n : int
        Maximum matches return karne hain (default 5)
    
    Returns:
    --------
    list : Matching lost items with similarity scores
    """
    
    # QuerySet ko list mein convert karna
    lost_items = list(lost_items_queryset)
    
    # Similar items dhundna
    matches = get_similar_items(found_item, lost_items, top_n=top_n)
    
    # Threshold se filter karna
    filtered_matches = [
        match for match in matches 
        if match['similarity_score'] >= threshold
    ]
    
    return filtered_matches


def calculate_match_score(item1, item2):
    """
    Do items ke beech match score calculate karta hai.
    Individual comparison ke liye useful hai.
    
    Parameters:
    -----------
    item1 : Item
        Pehli item
    item2 : Item
        Doosri item
    
    Returns:
    --------
    float : Similarity score as percentage (0-100)
    """
    
    # Dono items ka text prepare karna
    text1 = prepare_item_text(item1)
    text2 = prepare_item_text(item2)
    
    # Vectorizer initialize karna
    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),
        lowercase=True,
    )
    
    try:
        # TF-IDF vectors banana
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        
        # Cosine similarity calculate karna
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        # Percentage mein convert kar ke return karna
        return round(similarity * 100, 2)
        
    except Exception as e:
        print(f"Error calculating match score: {e}")
        return 0.0
