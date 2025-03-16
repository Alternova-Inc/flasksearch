/**
 * API Client for connecting to the Flask Search backend
 */

// Load environment variables from .env file
function loadEnv() {
  const env = {};
  try {
    // Check if window.ENV is already defined (could be injected server-side)
    if (window.ENV) return window.ENV;
    
    // Otherwise, try to load from localStorage (set by .env.js)
    const storedEnv = localStorage.getItem('app_env');
    if (storedEnv) {
      return JSON.parse(storedEnv);
    }
  } catch (error) {
    console.error('Error loading environment variables:', error);
  }
  return env;
}

// Get API configuration
function getApiConfig() {
  const env = loadEnv();
  return {
    baseUrl: env.API_URL || 'http://localhost:5000',
    apiToken: env.API_TOKEN || ''
  };
}

// Function to handle API errors
function handleApiError(error) {
  console.error('API Error:', error);
  return {
    html: `<div class="p-4 text-center text-red-500">Error: ${error.message || 'Failed to connect to API'}</div>`,
    meta: {
      count: 0,
      time_ms: 0,
      error: true
    }
  };
}

// Function to render HTML for items
function renderItems(items) {
  if (!items || items.length === 0) {
    return `<div class="p-4 text-center text-gray-500">No results found</div>`;
  }
  
  return items.map(item => `
    <div class="p-4 border-b border-gray-200 suggestion-item">
      <div class="font-medium">${item.name}</div>
      <div class="text-sm text-gray-600">${item.description || ''}</div>
      <div class="text-sm text-gray-500">${item.address || ''}</div>
      ${item.tags && item.tags.length > 0 ? `<div class="mt-1 flex flex-wrap gap-1">
        ${item.tags.map(tag => `<span class="px-2 py-1 text-xs bg-gray-100 rounded-full">${tag}</span>`).join('')}
      </div>` : ''}
    </div>
  `).join('');
}

// Main function to handle search
async function handleSearch(query, zipcode) {
  const startTime = performance.now();
  const { baseUrl, apiToken } = getApiConfig();
  
  try {
    // Prepare request URL with query parameters
    const url = new URL(`${baseUrl}/api/v1/suggestions`);
    
    // Add query parameters
    if (query) url.searchParams.append('query', query);
    if (zipcode) url.searchParams.append('zipcode', zipcode);
    
    // Prepare request headers
    const headers = {
      'Accept': 'application/json'
    };
    
    // Add API token if available
    if (apiToken) {
      headers['X-API-Token'] = apiToken;
    }
    
    console.log('Making API request to:', url.toString());
    console.log('With headers:', headers);
    
    // Make the API request (GET instead of POST)
    const response = await fetch(url, {
      method: 'GET',
      headers: headers,
      mode: 'cors',
      credentials: 'same-origin'
    });
    
    // Check if response is ok
    if (!response.ok) {
      throw new Error(`API returned ${response.status}: ${response.statusText}`);
    }
    
    // Parse response
    const data = await response.json();
    console.log('API response:', data);
    
    // Calculate time taken
    const endTime = performance.now();
    const timeTaken = Math.round(endTime - startTime);
    
    // Return formatted response
    return {
      html: renderItems(data.items || []),
      meta: {
        count: data.meta ? data.meta.count : (data.items ? data.items.length : 0),
        time_ms: data.meta ? data.meta.time_ms : timeTaken,
        query: data.meta ? data.meta.query : query,
        zipcode: data.meta ? data.meta.zipcode : zipcode,
        total: data.meta ? data.meta.total : (data.items ? data.items.length : 0)
      }
    };
  } catch (error) {
    return handleApiError(error);
  }
}

// Export for use in other files
window.apiClient = {
  handleSearch
}; 