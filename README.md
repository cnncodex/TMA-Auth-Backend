# TMA-Auth-Backend
### Telegram Mini App Authenticate with intidata | Flask backend

## ☘️ Frontend examples
```javascript
const tg = window.Telegram.WebApp;
tg.ready();
const initData = tg.initData || "";

// Check if there is any init data
if (initData) {
  // Encode the initdata using Base64 to create an authorization token
  const authToken = btoa(initData);

  // Function to fetch data from an API
  async function fetchData() {
    try {
      const response = await fetch("https://api-endpoint.com", {
        method: "GET", 
        // Set the Authorization header with the Bearer token
        headers: {
          "Authorization": `Bearer ${authToken}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        // console.log("Data fetched successfully:", data);
      } else {
        console.error("Failed to fetch data:", response.status, response.statusText);
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  }
  fetchData();
} else {
  console.log("No initdata available.");
}

```

## 🏖 if you have questions | Contact Me
[![profile](https://img.shields.io/badge/Contact%20me-On%20Telegram-blue)](https://t.me/cnncodex)
