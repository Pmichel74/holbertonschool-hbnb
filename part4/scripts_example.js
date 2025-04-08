/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

// Function to handle user login
async function userLogin(email, password) {
    try {
      const response = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });
  
      if (response.ok) {
        const data = await response.json();
        document.cookie = `token=${data.access_token}; path=/`;
        window.location.href = "index.html";
      } else {
        alert("Login failed: " + response.statusText);
      }
    } catch (error) {
      console.error("Error during login:", error);
    }
  }
  
  // Function to get a specific cookie by name
  function getCookie(name) {
    const allCookies = document.cookie
      .split(";")
      .find((row) => row.trim().startsWith(`${name}=`));
    return allCookies ? allCookies.split("=")[1] : null;
  }
  
  // Function to check if the user is authenticated
  async function checkAuthentication() {
    const token = getCookie("token");
    const loginLink = document.getElementById("login-link");
  
    if (!token) {
      loginLink.style.display = "block";
    } else {
      loginLink.style.display = "none";
      const places = await fetchPlaces(token);
      displayPlaces(places);
    }
  }
  
  // Function to fetch places data
  async function fetchPlaces(token) {
    try {
      const response = await fetch("http://127.0.0.1:5000/places", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `${token}`,
        },
      });
  
      if (response.ok) {
        return await response.json();
      } else {
        console.error("Failed to fetch places");
        return [];
      }
    } catch (error) {
      console.error("Error fetching places:", error);
      return [];
    }
  }
  
  //Fetch specific place details
  async function fetchPlace(placeID) {
    try {
      const response = await fetch(`http://127.0.0.1:5000/places/${placeID}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });
  
      if (response.ok) {
        // console.log(response);
        return await response.json();
      } else {
        console.error("Failed to fetch place");
        return [];
      }
    } catch (error) {
      console.error("Error fetching place:", error);
      return [];
    }
  }
  
  // Redirect to places
  function displayDetails(placeDetails) {
    // console.log(placeDetails);
    localStorage.setItem("placeDetails", JSON.stringify(placeDetails));
    window.location.href = "place.html";
  }
  
  //getPlaceID
  async function getPlaceID(placeID) {
    console.log(placeID);
    const placeDetails = await fetchPlace(placeID);
    displayDetails(placeDetails);
  }
  
  // Function to display places dynamically in the DOM
  function displayPlaces(places) {
    const placesList = document.getElementById("places-list");
    if (placesList) {
      placesList.innerHTML = "";
    }
  
    let row;
    places.forEach((place, index) => {
      if (index % 5 === 0) {
        row = document.createElement("div");
        row.className = "child-row";
        placesList.appendChild(row);
      }
  
      const column = document.createElement("div");
      column.className = "child-row-col";
  
      const link = document.createElement("a");
      link.className = "link-wrapper";
      link.dataset.placeId = place.id;
      link.href = "#";
      link.addEventListener("click", (event) => {
        event.preventDefault();
        const placeID = event.currentTarget.dataset.placeId;
        getPlaceID(placeID);
      });
      
  
      const placeCard = document.createElement("div");
      placeCard.className = "place-card";
  
      const imageWrapper = document.createElement("div");
      imageWrapper.className = "image-wrapper";
  
      const placeImage = document.createElement("div");
      placeImage.className = "place-image";
      placeImage.textContent = "Image Here";
      imageWrapper.appendChild(placeImage);
  
      const cardContent = document.createElement("div");
      cardContent.className = "card-content";
  
      const nameHeading = document.createElement("h3");
      nameHeading.className = "card-content-text";
      nameHeading.textContent = place.id;
      cardContent.appendChild(nameHeading);
  
      const priceParagraph = document.createElement("p");
      priceParagraph.className = "card-content-text";
      priceParagraph.textContent = `Price Per Night: $${place.price_per_night}`;
      cardContent.appendChild(priceParagraph);
  
      const locationParagraph = document.createElement("p");
      locationParagraph.className = "card-content-text";
      locationParagraph.textContent = `Location: ${place.city_name}`;
      cardContent.appendChild(locationParagraph);
  
      placeCard.appendChild(imageWrapper);
      placeCard.appendChild(cardContent);
      link.appendChild(placeCard);
      column.appendChild(link);
      row.appendChild(column);
    });
  }
  
  // DOM Content Loaded Function
  document.addEventListener("DOMContentLoaded", () => {
    // Handle user login
    const loginForm = document.getElementById("login-form");
    if (loginForm) {
      loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        await userLogin(email, password);
      });
    }
  
    // Check user authentication on window load
    window.addEventListener("load", checkAuthentication);
  
    //Display place details dynamically
    
    
  
    // Handle country filter change (if needed)
    const countryFilter = document.getElementById('country-filter');
    if (countryFilter) {
      countryFilter.addEventListener('change', (event) => {
        // Your event handler code
      });
    }
  });
    