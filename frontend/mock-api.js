/**
 * Mock API for search suggestions
 * This file simulates the API response until the real endpoint is implemented
 */

// Sample data for suggestions
const sampleData = [
  { id: 1, name: "Cafe Delight", category: "Cafe", tags: ["coffee", "breakfast", "wifi"] },
  { id: 2, name: "Burger Palace", category: "Restaurant", tags: ["burgers", "fast food", "takeout"] },
  { id: 3, name: "Sushi Express", category: "Restaurant", tags: ["sushi", "japanese", "healthy"] },
  { id: 4, name: "Pizza Corner", category: "Restaurant", tags: ["pizza", "italian", "delivery"] },
  { id: 5, name: "Green Salad Bar", category: "Restaurant", tags: ["salad", "healthy", "vegan"] },
  { id: 6, name: "Coffee House", category: "Cafe", tags: ["coffee", "pastries", "quiet"] },
  { id: 7, name: "Taco Fiesta", category: "Restaurant", tags: ["mexican", "tacos", "spicy"] },
  { id: 8, name: "Noodle Shop", category: "Restaurant", tags: ["noodles", "asian", "quick"] },
  { id: 9, name: "Ice Cream Parlor", category: "Dessert", tags: ["ice cream", "dessert", "family"] },
  { id: 10, name: "Cocktail Lounge", category: "Bar", tags: ["cocktails", "nightlife", "upscale"] }
];

// Function to simulate API response delay
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Function to filter suggestions based on query
function filterSuggestions(query) {
  if (!query) return [];
  
  const lowerQuery = query.toLowerCase();
  return sampleData.filter(item => {
    // Check if query matches name
    if (item.name.toLowerCase().includes(lowerQuery)) return true;
    
    // Check if query matches category
    if (item.category.toLowerCase().includes(lowerQuery)) return true;
    
    // Check if query matches any tags
    return item.tags.some(tag => tag.toLowerCase().includes(lowerQuery));
  });
}

// Function to render HTML for suggestions
function renderSuggestions(suggestions) {
  if (suggestions.length === 0) {
    return `<div class="p-4 text-center text-gray-500">No suggestions found</div>`;
  }
  
  return suggestions.map(item => `
    <div class="p-4 border-b border-gray-200 suggestion-item">
      <div class="font-medium">${item.name}</div>
      <div class="text-sm text-gray-600">Category: ${item.category}</div>
      ${item.tags.length > 0 ? `<div class="mt-1 flex flex-wrap gap-1">
        ${item.tags.map(tag => `<span class="px-2 py-1 text-xs bg-gray-100 rounded-full">${tag}</span>`).join('')}
      </div>` : ''}
    </div>
  `).join('');
}

// Main function to handle search
async function handleSearch(query) {
  const startTime = performance.now();
  
  // Simulate network delay (100-300ms)
  await delay(Math.random() * 200 + 100);
  
  // Filter suggestions
  const suggestions = filterSuggestions(query);
  
  // Calculate time taken
  const endTime = performance.now();
  const timeTaken = Math.round(endTime - startTime);
  
  // Return response
  return {
    html: renderSuggestions(suggestions),
    meta: {
      count: suggestions.length,
      time_ms: timeTaken,
      query: query
    }
  };
}

// Export for use in other files
window.mockApi = {
  handleSearch
}; 