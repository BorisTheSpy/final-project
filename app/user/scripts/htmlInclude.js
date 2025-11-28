/**
 * HTML Include Script
 * Dynamically loads and inserts HTML content from external files
 *
 * Usage:
 *   <div data-include="path/to/file.html"></div>
 *   <header data-include="components/header.html"></header>
 */

(function () {
  "use strict";

  /**
   * Resolves a relative path based on the current page's location
   * @param {string} includePath - The path specified in data-include attribute
   * @returns {string} - Resolved absolute path
   */
  function resolvePath(includePath) {
    // If the path starts with /, it's already absolute
    if (includePath.startsWith("/")) {
      return includePath;
    }

    // Get the current page's directory
    const currentPath = window.location.pathname;
    const currentDir = currentPath.substring(
      0,
      currentPath.lastIndexOf("/") + 1
    );

    // Resolve relative path
    const parts = currentDir.split("/").filter((p) => p);
    const includeParts = includePath.split("/").filter((p) => p);

    // Handle .. and . in the path
    for (let part of includeParts) {
      if (part === "..") {
        parts.pop();
      } else if (part !== ".") {
        parts.push(part);
      }
    }

    return "/" + parts.join("/");
  }

  /**
   * Loads HTML content from a file and inserts it into the target element
   * @param {HTMLElement} element - The element to insert content into
   * @param {string} filePath - Path to the HTML file to load
   */
  async function loadInclude(element, filePath) {
    try {
      const resolvedPath = resolvePath(filePath);
      const response = await fetch(resolvedPath);

      if (!response.ok) {
        throw new Error(
          `Failed to load ${filePath}: ${response.status} ${response.statusText}`
        );
      }

      const html = await response.text();
      element.innerHTML = html;

      // Dispatch a custom event to notify that the include was loaded
      element.dispatchEvent(
        new CustomEvent("includeLoaded", {
          detail: { path: filePath, element: element },
        })
      );
    } catch (error) {
      console.error(`Error loading include "${filePath}":`, error);
      element.innerHTML = `<p style="color: red;">Error loading ${filePath}</p>`;
    }
  }

  /**
   * Initialize the include system
   */
  function initIncludes() {
    const elements = document.querySelectorAll("[data-include]");

    if (elements.length === 0) {
      return;
    }

    // Load all includes in parallel
    const promises = Array.from(elements).map((element) => {
      const filePath = element.getAttribute("data-include");
      return loadInclude(element, filePath);
    });

    // Wait for all includes to complete
    Promise.all(promises).then(() => {
      // Dispatch a custom event when all includes are loaded
      document.dispatchEvent(new CustomEvent("allIncludesLoaded"));
    });
  }

  // Initialize when DOM is ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initIncludes);
  } else {
    // DOM is already ready
    initIncludes();
  }
})();
