/**
 * Menu Display Script
 * Fetches sandwiches from the API and displays them in a 3-column grid
 */

(function () {
  "use strict";

  const API_URL = "http://localhost:8000/sandwiches";
  const MENU_CONTAINER_ID = "menu-container";

  /**
   * Formats a price as currency
   * @param {number} price - The price to format
   * @returns {string} - Formatted price string
   */
  function formatPrice(price) {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
    }).format(price);
  }

  /**
   * Creates a menu item card element
   * @param {Object} sandwich - Sandwich object with id, sandwich_name, and price
   * @returns {HTMLElement} - Menu item card element
   */
  function createMenuItemCard(sandwich) {
    const card = document.createElement("div");
    card.className = "menu-item-card";
    card.setAttribute("data-sandwich-id", sandwich.id);

    const name = document.createElement("h3");
    name.className = "menu-item-name";
    name.textContent = sandwich.sandwich_name || "Unnamed Sandwich";

    const price = document.createElement("p");
    price.className = "menu-item-price";
    price.textContent = formatPrice(parseFloat(sandwich.price));

    card.appendChild(name);
    card.appendChild(price);

    return card;
  }

  /**
   * Displays loading state
   * @param {HTMLElement} container - Container element
   */
  function showLoading(container) {
    container.innerHTML = '<p class="loading-message">Loading menu...</p>';
  }

  /**
   * Displays error state
   * @param {HTMLElement} container - Container element
   * @param {string} message - Error message
   */
  function showError(container, message) {
    container.innerHTML = `<p class="error-message">Error: ${message}</p>`;
  }

  /**
   * Fetches sandwiches from the API and displays them
   */
  async function loadMenu() {
    const container = document.getElementById(MENU_CONTAINER_ID);

    if (!container) {
      console.error(`Menu container with id "${MENU_CONTAINER_ID}" not found`);
      return;
    }

    showLoading(container);

    try {
      const response = await fetch(API_URL);

      if (!response.ok) {
        throw new Error(
          `Failed to load menu: ${response.status} ${response.statusText}`
        );
      }

      const sandwiches = await response.json();

      if (!Array.isArray(sandwiches)) {
        throw new Error("Invalid response format from API");
      }

      // Clear loading message
      container.innerHTML = "";

      if (sandwiches.length === 0) {
        container.innerHTML =
          '<p class="empty-message">No menu items available.</p>';
        return;
      }

      // Create and append menu item cards
      sandwiches.forEach((sandwich) => {
        const card = createMenuItemCard(sandwich);
        container.appendChild(card);
      });

      // Dispatch custom event when menu is loaded
      document.dispatchEvent(
        new CustomEvent("menuLoaded", {
          detail: { sandwiches: sandwiches },
        })
      );
    } catch (error) {
      console.error("Error loading menu:", error);
      showError(container, error.message);
    }
  }

  // Initialize menu when DOM is ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", loadMenu);
  } else {
    // DOM is already ready
    loadMenu();
  }
})();

