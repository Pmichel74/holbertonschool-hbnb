/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
  // Attendre que le DOM soit complètement chargé avant d'exécuter le script
  
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
});

// Fonction asynchrone pour effectuer la requête à l'API de login
async function loginUser(email, password) {
  try {
    console.log('Attempting to login with:', email);
    
    // SIMULATION DE CONNEXION RÉUSSIE POUR TEST
    // Pour les besoins du test, nous simulons une connexion réussie
    // Une fois que vous avez un vrai backend, supprimez ces lignes
    console.log('Simulating successful login');
    document.cookie = `token=simulated-jwt-token; path=/`;
    window.location.href = 'index.html';
    return; // Arrête l'exécution ici
    
    const response = await fetch('/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });
    
    // Traitement de la réponse
    if (response.ok) {
      const data = await response.json();
      console.log('Login successful, storing token');
      document.cookie = `token=${data.token}; path=/`;
      window.location.href = 'index.html';
    } else {
      console.log('Login failed:', response.statusText);
      throw new Error(`Login failed: ${response.statusText}`);
    }
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
}