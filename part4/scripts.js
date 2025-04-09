/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
  // Attendre que le DOM soit complètement chargé avant d'exécuter le script
  
  // Vérifier l'authentification de l'utilisateur au chargement de la page
  checkAuthentication();
  
  // Récupération de la liste des places
  fetchPlaces();
  
  // Remplir le menu déroulant de filtre de prix avec les options
  populatePriceFilter();
  
  // Récupération du formulaire de connexion en utilisant son ID
  const loginForm = document.getElementById('login-form');
  
  // Vérification que le formulaire existe bien dans le DOM
  if (loginForm) {
    console.log('Login form found, adding event listener');
    // Ajout d'un écouteur d'événement qui se déclenche lors de la soumission du formulaire
    loginForm.addEventListener('submit', async (event) => {
      // Empêche le comportement par défaut du navigateur (rechargement de page et envoi des données)
      event.preventDefault();
      console.log('Form submission prevented');
      
      // Récupération des valeurs saisies par l'utilisateur
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      console.log('Email:', email);
      
      // Utilisation de la fonction asynchrone pour faire la requête API
      try {
        await loginUser(email, password);
      } catch (error) {
        console.error('Error during login:', error);
        const errorMessage = document.getElementById('error-message');
        if (errorMessage) {
          errorMessage.textContent = 'An error occurred during login. Please try again.';
          errorMessage.style.display = 'block';
        } else {
          // Création d'un élément message d'erreur s'il n'existe pas
          const newErrorMessage = document.createElement('div');
          newErrorMessage.id = 'error-message';
          newErrorMessage.textContent = 'An error occurred during login. Please try again.';
          newErrorMessage.style.color = 'red';
          newErrorMessage.style.marginTop = '10px';
          newErrorMessage.style.textAlign = 'center';
          loginForm.appendChild(newErrorMessage);
        }
      }
    });
  } else {
    // Message d'erreur si le formulaire n'est pas trouvé dans le DOM
    console.error("Login form not found in the page");
  }
  
  // Ajouter un écouteur d'événement sur le filtre de prix
  const priceFilter = document.getElementById('price-filter');
  if (priceFilter) {
    priceFilter.addEventListener('change', filterPlacesByPrice);
  }

  // Vérification explicite de l'élément places-list
  const placesList = document.getElementById('places-list');
  console.log('Places list element found:', placesList);
});

/**
 * Fonction pour récupérer la valeur d'un cookie par son nom
 * @param {string} name - Nom du cookie à récupérer
 * @returns {string|null} - Valeur du cookie ou null si non trouvé
 */
function getCookie(name) {
    // Function to get a cookie value by its name
    const cookies = document.cookie.split('; ');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].split('=');
        if (cookie[0] === name) {
            return cookie[1];
        }
    }
    return null;
}

/**
 * Vérifier si l'utilisateur est authentifié et contrôle la visibilité des liens de navigation
 * Redirige vers la page de connexion si l'utilisateur n'est pas authentifié et est sur la page d'index
 */
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.querySelector('.login-button');
    const logoutLink = document.querySelector('.logout-button');
    const isIndexPage = window.location.pathname.endsWith('index.html') || 
                        window.location.pathname.endsWith('/') ||
                        window.location.pathname.endsWith('/part4/');

    if (!token) {
        // L'utilisateur n'est pas authentifié
        if (loginLink) {
            loginLink.style.display = 'block';
        }
        if (logoutLink) {
            logoutLink.style.display = 'none';
        }
        
        // Rediriger vers la page de login si on est sur la page principale
        if (isIndexPage) {
            console.log('User not authenticated, redirecting to login page');
            window.location.href = 'login.html';
            return false;
        }
    } else {
        // L'utilisateur est authentifié
        if (loginLink) {
            loginLink.style.display = 'none';
        }
        if (logoutLink) {
            logoutLink.style.display = 'block';
            // Ajouter un écouteur d'événement pour la déconnexion
            logoutLink.addEventListener('click', logout);
        }
        
        // Fetch places data if the user is authenticated and on the index page
        if (isIndexPage) {
            fetchPlaces(token);
        }
        return true;
    }
}

// Fonction asynchrone pour effectuer la requête à l'API de login
async function loginUser(email, password) {
  try {
    console.log('Attempting to login with:', email);
    
    // MODE DÉVELOPPEMENT: Activer cette ligne pour simuler une connexion réussie
    const devMode = false; // Changer à false pour utiliser le vrai backend
    
    if (devMode) {
      console.log('DEVELOPMENT MODE: Simulating successful login');
      // Simulation d'une pause réseau
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Enregistrement d'un token fictif
      document.cookie = `token=dev-jwt-token; path=/; max-age=86400`;
      
      // Redirection vers la page d'accueil
      window.location.href = 'index.html';
      return;
    }
    
    // Code normal pour la communication avec le backend
    const response = await fetch('http://localhost:5000/api/v1/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include', // Ensure cookies are included in the request
      body: JSON.stringify({ email, password })
    });
    
    // Traitement de la réponse
    if (response.ok) {
      const data = await response.json();
      console.log('Login successful, storing token');
      
      // Le backend renvoie access_token et non token
      const token = data.access_token;
      
      if (!token) {
        console.error('Token not found in response');
        throw new Error('Authentication failed: Invalid server response');
      }
      
      // Stockage du JWT token dans un cookie pour la gestion de session
      document.cookie = `token=${token}; path=/; max-age=86400`; // Expire après 24 heures
      
      // Redirection vers la page d'accueil après connexion réussie
      window.location.href = 'index.html';
    } else {
      // Afficher le message d'erreur dans l'interface
      const errorDiv = document.getElementById('login-error');
      if (errorDiv) {
        errorDiv.textContent = 'Identifiants invalides, veuillez réessayer.';
        errorDiv.style.display = 'block';
      }
      
      // Pour le debugging en console
      if (response.status === 401) {
        console.error('Login failed: Invalid credentials');
      } else {
        console.error(`Login failed with status: ${response.status}`);
        try {
          const errorData = await response.json();
          console.error('Error details:', errorData);
        } catch (e) {
          console.error('No JSON response from server');
        }
      }
      
      throw new Error(`Authentication failed: ${response.statusText}`);
    }
  } catch (error) {
    console.error('Login error:', error);
    
    // Afficher le message d'erreur à l'utilisateur
    const errorDiv = document.getElementById('login-error');
    if (errorDiv) {
      errorDiv.textContent = 'Échec de connexion. Veuillez réessayer.';
      errorDiv.style.display = 'block';
    }
    
    throw error;
  }
}

/**
 * Fonction pour récupérer la liste des places depuis l'API
 */
async function fetchPlaces(token) {
    try {
        console.log('Attempting to fetch places with token:', token);

        // Vérifier si le conteneur des places existe avant de continuer
        const placesList = document.getElementById('places-list');
        if (!placesList) {
            console.log('Places list container not found, probably not on index page');
            return; // Ne pas continuer si on n'est pas sur la page d'index
        }

        const headers = {
            'Content-Type': 'application/json'
        };

        // Add Authorization header only if token is available
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch('http://localhost:5000/api/v1/places/', {
            method: 'GET',
            headers: headers,
            credentials: 'include' // Include cookies
        });

        console.log('Places response status:', response.status);

        if (response.ok) {
            const data = await response.json();
            console.log('Places data received:', data);

            if (data && Array.isArray(data)) {
                displayPlaces(data);
                window.allPlaces = data;
            } else {
                console.error('Invalid places data format:', data);
                throw new Error('Invalid data format received from server');
            }
        } else {
            console.error('Failed to fetch places:', response.status, response.statusText);
            if (response.status === 401 || response.status === 403) {
                console.log('Authentication issue but continuing to show index page');
            }
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

/**
 * Fonction pour afficher les places dans la section #places-list
 * @param {Array} places - Liste des places à afficher
 */
function displayPlaces(places) {
    // Ajouter du débogage pour voir les données reçues
    console.log('Raw places data to display:', places);

    // Clear the current content of the places list
    const placesList = document.getElementById('places-list');
    if (!placesList) {
        console.error('Places list element not found');
        return;
    }

    placesList.innerHTML = '';

    if (!places || places.length === 0) {
        placesList.innerHTML = '<p style="text-align: center; margin-top: 20px;">Aucune place disponible pour le moment.</p>';
        return;
    }

    // Iterate over the places data
    places.forEach(place => {
        // For each place, create a div element and set its content
        const placeElement = document.createElement('div');
        placeElement.classList.add('place-card');
        placeElement.classList.add('place');

        // Récupérer les champs selon le format du backend (modifié pour correspondre à la nouvelle API)
        const id = place.id || '';
        const title = place.name || place.title || 'Sans nom'; // Support des deux nommages
        const description = place.description || 'Pas de description disponible';
        const location = place.location || `${place.latitude || ''}, ${place.longitude || ''}`;
        const price = place.price || 0;

        console.log('Processing place:', { id, title, description, location, price });

        // Store the price as data attributes for filtering
        placeElement.dataset.price = price;
        
        placeElement.innerHTML = `
            <h2>${title}</h2>
            <p class="description">${description}</p>
            <p class="location">${location}</p>
            <p class="price"><strong>Price:</strong> ${price ? '$' + price : 'Not specified'}</p>
            <button class="details-button" data-id="${id}">View Details</button>
        `;
        
        // Append the created element to the places list
        placesList.appendChild(placeElement);
    });

    // Appliquer le filtre initial si un prix est déjà sélectionné
    filterPlacesByPrice();

    // Ajouter des écouteurs d'événements aux boutons de détails
    document.querySelectorAll('.details-button').forEach(button => {
        button.addEventListener('click', function() {
            const placeId = this.getAttribute('data-id');
            if (placeId) {
                window.location.href = `place.html?id=${placeId}`;
            }
        });
    });
}

/**
 * Fonction pour filtrer les places en fonction du prix sélectionné
 */
function filterPlacesByPrice() {
  const priceFilter = document.getElementById('price-filter');
  if (!priceFilter) return;
  
  const selectedPrice = priceFilter.value || 'all';
  console.log('Filtering places by price:', selectedPrice);
  
  // Sélectionner toutes les places
  const places = document.querySelectorAll('.place-card, .place');
  
  places.forEach(place => {
    const placePrice = parseInt(place.dataset.price) || 0;
    console.log('Place price:', placePrice, 'Selected price:', selectedPrice);
    
    if (selectedPrice === 'all') {
      place.style.display = 'block'; // Toujours afficher si "all" est sélectionné
    } else {
      const maxPrice = parseInt(selectedPrice);
      place.style.display = placePrice <= maxPrice ? 'block' : 'none';
    }
  });
}

/**
 * Fonction pour remplir le menu déroulant de filtre de prix avec les options
 */
function populatePriceFilter() {
  const priceFilter = document.getElementById('price-filter');
  if (priceFilter) {
    // Options as specified in the requirements
    const options = [
      { value: '10', text: '10' },
      { value: '50', text: '50' },
      { value: '100', text: '100' },
      { value: 'all', text: 'All' }
    ];

    // Add options to select element
    options.forEach(option => {
      const optionElement = document.createElement('option');
      optionElement.value = option.value;
      optionElement.textContent = option.text;
      priceFilter.appendChild(optionElement);
    });

    // Default selection - explicitement sélectionner "All" pour éviter les places masquées
    priceFilter.value = 'all';

    // Déclencher un changement pour appliquer le filtre initial
    const event = new Event('change');
    priceFilter.dispatchEvent(event);
  }
}

/**
 * Fonction pour déconnecter l'utilisateur
 * @param {Event} event - L'événement de clic
 */
function logout(event) {
  event.preventDefault();  // Empêcher le comportement par défaut du lien
  document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";  // Supprimer le token en définissant une date d'expiration dans le passé
  console.log('User logged out successfully');
  window.location.href = 'login.html';  // Rediriger vers la page de connexion
}