/**
 * Mock API for search suggestions
 * This file simulates the API response until the real endpoint is implemented
 */

// Sample data for suggestions with location data
const sampleData = [
  { id: 1, name: "Cafe Delight", category: "Cafe", tags: ["coffee", "breakfast", "wifi"], location: { zip: "10001", lat: 40.7506, lng: -73.9971 } },
  { id: 2, name: "Burger Palace", category: "Restaurant", tags: ["burgers", "fast food", "takeout"], location: { zip: "10002", lat: 40.7168, lng: -73.9861 } },
  { id: 3, name: "Sushi Express", category: "Restaurant", tags: ["sushi", "japanese", "healthy"], location: { zip: "10003", lat: 40.7335, lng: -73.9903 } },
  { id: 4, name: "Pizza Corner", category: "Restaurant", tags: ["pizza", "italian", "delivery"], location: { zip: "10004", lat: 40.7046, lng: -74.0121 } },
  { id: 5, name: "Green Salad Bar", category: "Restaurant", tags: ["salad", "healthy", "vegan"], location: { zip: "10005", lat: 40.7047, lng: -74.0085 } },
  { id: 6, name: "Coffee House", category: "Cafe", tags: ["coffee", "pastries", "quiet"], location: { zip: "10006", lat: 40.7074, lng: -74.0113 } },
  { id: 7, name: "Taco Fiesta", category: "Restaurant", tags: ["mexican", "tacos", "spicy"], location: { zip: "10007", lat: 40.7127, lng: -74.0059 } },
  { id: 8, name: "Noodle Shop", category: "Restaurant", tags: ["noodles", "asian", "quick"], location: { zip: "10008", lat: 40.7587, lng: -73.9787 } },
  { id: 9, name: "Ice Cream Parlor", category: "Dessert", tags: ["ice cream", "dessert", "family"], location: { zip: "10009", lat: 40.7264, lng: -73.9818 } },
  { id: 10, name: "Cocktail Lounge", category: "Bar", tags: ["cocktails", "nightlife", "upscale"], location: { zip: "10010", lat: 40.7387, lng: -73.9818 } }
];

// Function to simulate API response delay
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Function to calculate distance between two points (Haversine formula)
function calculateDistance(lat1, lon1, lat2, lon2) {
  const R = 6371; // Radius of the earth in km
  const dLat = deg2rad(lat2 - lat1);
  const dLon = deg2rad(lon2 - lon1);
  const a = 
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * 
    Math.sin(dLon/2) * Math.sin(dLon/2); 
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
  const distance = R * c; // Distance in km
  return distance;
}

function deg2rad(deg) {
  return deg * (Math.PI/180);
}

// Function to get coordinates for a zipcode (mock implementation)
function getZipCodeCoordinates(zipcode) {
  // In a real implementation, this would call a geocoding service
  // For mock purposes, we'll return New York coordinates if not found
  const item = sampleData.find(item => item.location.zip === zipcode);
  if (item) {
    return { lat: item.location.lat, lng: item.location.lng };
  }
  // Default to Manhattan coordinates
  return { lat: 40.7831, lng: -73.9712 };
}

// Function to filter suggestions based on query
function filterSuggestions(query, zipcode) {
  if (!query && !zipcode) return [];
  
  let results = sampleData;
  
  // Filter by query if provided
  if (query) {
    const lowerQuery = query.toLowerCase();
    results = results.filter(item => {
      // Check if query matches name
      if (item.name.toLowerCase().includes(lowerQuery)) return true;
      
      // Check if query matches category
      if (item.category.toLowerCase().includes(lowerQuery)) return true;
      
      // Check if query matches any tags
      return item.tags.some(tag => tag.toLowerCase().includes(lowerQuery));
    });
  }
  
  // Add distance if zipcode provided
  if (zipcode) {
    const coords = getZipCodeCoordinates(zipcode);
    
    results = results.map(item => {
      const distance = calculateDistance(
        coords.lat, coords.lng,
        item.location.lat, item.location.lng
      );
      
      return {
        ...item,
        distance_km: parseFloat(distance.toFixed(2))
      };
    });
    
    // Sort by distance
    results.sort((a, b) => a.distance_km - b.distance_km);
  }
  
  return results;
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
      ${item.distance_km ? `<div class="text-sm text-blue-600">Distance: ${item.distance_km} km</div>` : ''}
      ${item.tags.length > 0 ? `<div class="mt-1 flex flex-wrap gap-1">
        ${item.tags.map(tag => `<span class="px-2 py-1 text-xs bg-gray-100 rounded-full">${tag}</span>`).join('')}
      </div>` : ''}
    </div>
  `).join('');
}

// Main function to handle search
async function handleSearch(query, zipcode) {
  const startTime = performance.now();
  
  // Simulate network delay (100-300ms)
  await delay(Math.random() * 200 + 100);
  
  // Filter suggestions
  const suggestions = filterSuggestions(query, zipcode);
  
  // Calculate time taken
  const endTime = performance.now();
  const timeTaken = Math.round(endTime - startTime);
  
  // Return response
  return {
    html: renderSuggestions(suggestions),
    meta: {
      count: suggestions.length,
      time_ms: timeTaken,
      query: query,
      zipcode: zipcode
    }
  };
}

// Export for use in other files
window.mockApi = {
  handleSearch
}; 