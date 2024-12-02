from tavily import TavilyClient
import os
from dotenv import load_dotenv

class InstagramLeadGenerator:
    def __init__(self):
        env_path = os.path.join(os.getcwd(), '.env')
        
        # Read API key directly from file
        with open(env_path, 'r') as f:
            content = f.read().strip()
            api_key = content.split('=')[1]
        
        print(f"Using API key directly: {api_key}")
        self.leads = []
        self.tavily_client = TavilyClient(api_key=api_key)
    
    def generate_leads(self):
        # Get user input
        niche, location = self.get_user_input()
        print(f"\nSearching for {niche} Instagram accounts in {location}...")
        
        # Get search results
        results = self.search_instagram_accounts(niche, location)
        
        # Process and format the leads
        formatted_leads = []
        for result in results:
            title = result.get('title', '')
            content = result.get('content', '')
            url = result.get('url', '')
            
            # Extract Instagram handles from content
            handles = [word for word in content.split() if word.startswith('@')]
            
            # Store relevant information only if handles are found
            for handle in handles:
                lead = {
                    'source': title,
                    'description': content[:200],  # First 200 chars of content
                    'url': url,
                    'instagram_handle': handle
                }
                formatted_leads.append(lead)
        
        self.leads = formatted_leads
        
        # Print results in a readable format
        print("\nFound Leads:")
        for i, lead in enumerate(formatted_leads, 1):
            print(f"\n{i}. Source: {lead['source']}")
            print(f"   Description: {lead['description']}...")
            print(f"   URL: {lead['url']}")
            print(f"   Instagram Handle: {lead['instagram_handle']}")
        
        return formatted_leads
    
    def save_leads(self):
        pass
    
    def load_leads(self):
        pass
    
    def test_tavily_connection(self):
        try:
            # Test with a more relevant search
            response = self.tavily_client.search(
                query="top fitness instagram accounts in Los Angeles",
                search_depth="basic"
            )
            print("\nTavily API Connection Successful!")
            print("\nSample results:")
            
            # Ensure response is iterable
            if isinstance(response, list):
                # Print first 2 results in a readable format
                for i, result in enumerate(response[:2]):
                    print(f"\n{i+1}. Title: {result.get('title', 'N/A')}")
                    print(f"   Content: {result.get('content', 'N/A')[:200]}...")
            else:
                print("Unexpected response format:", response)
            
            return True
        except Exception as e:
            print(f"Error connecting to Tavily: {e}")
            return False
    
    def get_user_input(self):
        niche = input("Enter the niche (e.g., fitness, food, fashion): ").strip()
        location = input("Enter the location (e.g., Los Angeles, New York): ").strip()
        return niche, location
    
    def search_instagram_accounts(self, niche, location):
        try:
            # Broader query
            query = f"{niche} Instagram accounts in {location}"
            response = self.tavily_client.search(query=query, search_depth="deep")  # Keep search depth as "deep"
            
            print("\nSearch results:")
            if 'results' in response:
                for i, result in enumerate(response['results'][:15]):  # Show first 15 results
                    print(f"\n{i+1}. Title: {result.get('title', 'N/A')}")
                    print(f"   Content: {result.get('content', 'N/A')[:200]}...")
                    # Look for Instagram handles
                    content = result.get('content', '')
                    handles = [word for word in content.split() if word.startswith('@')]
                    if handles:
                        print(f"   Instagram handles found: {', '.join(handles)}")
            else:
                print("No results found in response")
            
            return response['results']
        except Exception as e:
            print(f"Error during search: {e}")
            return []
    
    def display_leads(self):
        if not self.leads:
            print("\nNo leads found!")
            return
        
        print("\n=== Current Leads ===")
        print(f"Total leads found: {len(self.leads)}")
        print("-------------------")
        
        for i, lead in enumerate(self.leads, 1):
            print(f"\nLead #{i}:")
            for key, value in lead.items():
                print(f"{key}: {value}")
            print("-------------------")

def main():
    generator = InstagramLeadGenerator()
    generator.generate_leads()
    generator.display_leads()

if __name__ == "__main__":
    main() 