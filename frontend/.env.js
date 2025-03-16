/**
 * This script loads environment variables from .env file
 * and makes them available to the frontend application
 */

(function() {
  // Default environment values
  const defaultEnv = {
    API_URL: 'http://localhost:5001',
    API_TOKEN: ''
  };

  // Function to parse .env file content
  function parseEnv(content) {
    const env = {};
    const lines = content.split('\n');
    
    for (const line of lines) {
      // Skip empty lines and comments
      if (!line || line.startsWith('#')) continue;
      
      // Parse key=value pairs
      const match = line.match(/^\s*([\w.-]+)\s*=\s*(.*)?\s*$/);
      if (match) {
        const key = match[1];
        let value = match[2] || '';
        
        // Remove quotes if present
        if (value.startsWith('"') && value.endsWith('"')) {
          value = value.slice(1, -1);
        }
        
        env[key] = value;
      }
    }
    
    return env;
  }
  
  // Function to load .env file
  async function loadEnvFile() {
    try {
      const response = await fetch('/.env');
      
      // If .env file is not found or access is denied, use defaults
      if (!response.ok) {
        console.warn('.env file not accessible, using default values');
        return defaultEnv;
      }
      
      const content = await response.text();
      const parsedEnv = parseEnv(content);
      
      // Merge with defaults (so any missing values use defaults)
      return { ...defaultEnv, ...parsedEnv };
    } catch (error) {
      console.error('Error loading .env file:', error);
      return defaultEnv;
    }
  }
  
  // Load environment variables and store them
  loadEnvFile().then(env => {
    // Store in localStorage for persistence
    localStorage.setItem('app_env', JSON.stringify(env));
    
    // Also make available globally
    window.ENV = env;
    
    console.log('Environment variables loaded:', env);
  });
})(); 