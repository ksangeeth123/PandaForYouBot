from googlesearch import search

def get_google_results(query, num_results=5):
    """
    Searches Google for the given query and returns a formatted string of results.
    """
    try:
        results = []
        # basic search yielding URLs
        # advanced=True yields generic Title/Description/URL objects in some versions, 
        # but standard search yields strings (URLs). 
        # checking library version behavior is important, but for simplicity we start with standard.
        # googlesearch-python (the one valid in pypi) often has 'search' returning strings.
        # There's another lib 'google' which is different. 
        # We'll assume the standard 'googlesearch-python' behavior which often just gives URLs unless using advanced.
        
        # improving to use advanced=True if available for better data, 
        # but let's stick to simple URL list first to avoid compat issues, 
        # then we can try to fetch titles if needed (or just return URLs).
        
        search_results = search(query, num_results=num_results, advanced=True)
        
        response_text = f"🔍 *Search Results for:* {query}\n\n"
        
        count = 0
        for result in search_results:
            count += 1
            # handling 'advanced' object if possible, otherwise it's a string
            if hasattr(result, 'title'): # It's a SearchResult object
                response_text += f"{count}. [{result.title}]({result.url})\n"
                response_text += f"_{result.description}_\n\n"
            else: # It's just a string URL
                response_text += f"{count}. {result}\n"
                
        if count == 0:
            return "No results found."
            
        return response_text
        
    except Exception as e:
        return f"An error occurred during search: {str(e)}"
