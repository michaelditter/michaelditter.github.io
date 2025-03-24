/**
 * Michael Ditter - Personal Branding Website
 * Main JavaScript File
 * 
 * This file handles all the interactive functionality of the website including:
 * - Navigation menu handling
 * - Scroll animations
 * - Testimonial slider
 * - Form submission
 * - Intersection Observer for animations
 */

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
  // Initialize all functionality
  initNavigation();
  initScrollAnimations();
  initTestimonialSlider();
  initContactForm();
  initIntersectionObserver();
  updateCopyrightYear();
  initFAQToggles();
  initNewsletterForm();
  initBitcoinReport();
  initAIReportSection();
});

/**
 * Mobile Navigation Toggle
 */
function initNavigation() {
  const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
  const navLinks = document.querySelector('.nav-links');
  
  if (mobileMenuToggle && navLinks) {
    mobileMenuToggle.addEventListener('click', function() {
      navLinks.classList.toggle('open');
      mobileMenuToggle.classList.toggle('active');
    });
    
    // Close mobile menu when clicking a link
    const links = navLinks.querySelectorAll('a');
    links.forEach(link => {
      link.addEventListener('click', function() {
        navLinks.classList.remove('open');
        mobileMenuToggle.classList.remove('active');
      });
    });
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(event) {
      if (!event.target.closest('.main-nav')) {
        navLinks.classList.remove('open');
        mobileMenuToggle.classList.remove('active');
      }
    });
  }
  
  // Add active class to navigation links based on scroll position
  const sections = document.querySelectorAll('section[id]');
  
  window.addEventListener('scroll', function() {
    let scrollPosition = window.scrollY;
    
    sections.forEach(section => {
      const headerHeight = document.querySelector('.site-header').offsetHeight;
      const extraPadding = 20; // Match the extraPadding from scroll function
      const sectionTop = section.offsetTop - headerHeight - extraPadding;
      const sectionHeight = section.offsetHeight;
      const sectionId = section.getAttribute('id');
      const correspondingNavLink = document.querySelector(`.nav-links a[href="#${sectionId}"]`);
      
      if (correspondingNavLink) {
        if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
          document.querySelectorAll('.nav-links a').forEach(link => {
            link.classList.remove('active');
          });
          correspondingNavLink.classList.add('active');
        }
      }
    });
  });
}

/**
 * Scroll-related animations and behaviors
 */
function initScrollAnimations() {
  const header = document.querySelector('.site-header');
  
  // Header shrink on scroll
  window.addEventListener('scroll', function() {
    if (window.scrollY > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });
  
  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]:not([href="#"])').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const targetId = this.getAttribute('href');
      const targetElement = document.querySelector(targetId);
      
      if (targetElement) {
        // Offset for fixed header - increase to prevent cutting off section headers
        const headerHeight = document.querySelector('.site-header').offsetHeight;
        const extraPadding = 20; // Additional padding to prevent text cutoff
        const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - headerHeight - extraPadding;
        
        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth'
        });
      }
    });
  });
}

/**
 * Testimonial slider functionality
 */
function initTestimonialSlider() {
  const testimonials = document.querySelectorAll('.testimonial');
  const dots = document.querySelectorAll('.dot');
  const prevButton = document.querySelector('.testimonials-navigation .prev');
  const nextButton = document.querySelector('.testimonials-navigation .next');
  
  if (testimonials.length === 0) return;
  
  let currentIndex = 0;
  
  // Hide all testimonials except the first one
  testimonials.forEach((testimonial, index) => {
    if (index !== 0) {
      testimonial.style.display = 'none';
    }
  });
  
  // Function to show a specific testimonial
  const showTestimonial = (index) => {
    testimonials.forEach((testimonial, i) => {
      testimonial.style.display = i === index ? 'block' : 'none';
    });
    
    dots.forEach((dot, i) => {
      dot.classList.toggle('active', i === index);
    });
    
    currentIndex = index;
  };
  
  // Next button click
  if (nextButton) {
    nextButton.addEventListener('click', () => {
      const newIndex = (currentIndex + 1) % testimonials.length;
      showTestimonial(newIndex);
    });
  }
  
  // Previous button click
  if (prevButton) {
    prevButton.addEventListener('click', () => {
      const newIndex = (currentIndex - 1 + testimonials.length) % testimonials.length;
      showTestimonial(newIndex);
    });
  }
  
  // Dot clicks
  dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
      showTestimonial(index);
    });
  });
  
  // Auto-advance testimonials every 5 seconds
  setInterval(() => {
    const newIndex = (currentIndex + 1) % testimonials.length;
    showTestimonial(newIndex);
  }, 5000);
}

/**
 * Contact form handling
 */
function initContactForm() {
  const contactForm = document.getElementById('contactForm');
  
  if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      // Simple validation
      let isValid = true;
      const requiredFields = contactForm.querySelectorAll('[required]');
      
      requiredFields.forEach(field => {
        if (!field.value.trim()) {
          isValid = false;
          field.classList.add('error');
        } else {
          field.classList.remove('error');
        }
      });
      
      // Email validation
      const emailField = contactForm.querySelector('#email');
      if (emailField && !isValidEmail(emailField.value) && emailField.value.trim()) {
        isValid = false;
        emailField.classList.add('error');
      }
      
      if (isValid) {
        // In a real implementation, this would send the form data to a server
        // For this demo, we'll just show a success message
        const formData = new FormData(contactForm);
        const formObject = {};
        
        formData.forEach((value, key) => {
          formObject[key] = value;
        });
        
        // Log form data to console for demo purposes
        console.log('Form submission data:', formObject);
        
        // Show success message (in a real implementation)
        const successMessage = document.createElement('div');
        successMessage.className = 'form-success';
        successMessage.textContent = 'Thank you! Your message has been sent successfully. I\'ll get back to you soon.';
        
        contactForm.innerHTML = '';
        contactForm.appendChild(successMessage);
      }
    });
  }
}

/**
 * Email validation helper
 */
function isValidEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

/**
 * Initialize Intersection Observer for animation on scroll
 */
function initIntersectionObserver() {
  // Check if IntersectionObserver is supported
  if ('IntersectionObserver' in window) {
    const elements = document.querySelectorAll(
      '.section-header, .about-text p, .hero-content, .expertise-card, .service-card, ' +
      '.insight-card, .testimonial, .speaking-text, .contact-form, .contact-info, .faq-item'
    );
    
    const options = {
      root: null, // Use viewport as root
      rootMargin: '0px',
      threshold: 0.1 // Trigger when 10% of the element is visible
    };
    
    const observer = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animated');
          // Once animated, no need to observe anymore
          observer.unobserve(entry.target);
        }
      });
    }, options);
    
    elements.forEach(element => {
      observer.observe(element);
    });
  } else {
    // Fallback for browsers that don't support IntersectionObserver
    const elements = document.querySelectorAll(
      '.section-header, .about-text p, .hero-content, .expertise-card, .service-card, ' +
      '.insight-card, .testimonial, .speaking-text, .contact-form, .contact-info, .faq-item'
    );
    
    elements.forEach(element => {
      element.classList.add('animated');
    });
  }
}

/**
 * Update copyright year to current year
 */
function updateCopyrightYear() {
  const yearElement = document.getElementById('currentYear');
  if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
  }
}

/**
 * Initialize FAQ toggles
 */
function initFAQToggles() {
  const faqToggles = document.querySelectorAll('.faq-toggle');
  
  faqToggles.forEach(toggle => {
    toggle.addEventListener('click', function() {
      const faqItem = this.closest('.faq-item');
      const answer = faqItem.querySelector('.faq-answer');
      
      // Toggle the active class on the item
      faqItem.classList.toggle('active');
      
      // Toggle the display of the answer
      if (faqItem.classList.contains('active')) {
        answer.style.maxHeight = answer.scrollHeight + 'px';
        this.innerHTML = '<img src="img/icons/minus.svg" alt="Collapse" width="24" height="24">';
      } else {
        answer.style.maxHeight = '0';
        this.innerHTML = '<img src="img/icons/plus.svg" alt="Expand" width="24" height="24">';
      }
    });
  });
}

/**
 * Analytics helper function (can be expanded as needed)
 * This is a placeholder for implementing analytics tracking
 */
function trackEvent(category, action, label) {
  // This would integrate with Google Analytics or other analytics platforms
  console.log(`Analytics event: ${category} - ${action} - ${label}`);
  
  // Example Google Analytics tracking code (commented out)
  /*
  if (typeof gtag === 'function') {
    gtag('event', action, {
      'event_category': category,
      'event_label': label
    });
  }
  */
}

/**
 * Helper for handling lazy loading of images via Intersection Observer
 * This is a more advanced implementation that could be used for performance optimization
 */
function initLazyLoading() {
  if ('IntersectionObserver' in window) {
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          
          // Optional: Load srcset as well if present
          if (img.dataset.srcset) {
            img.srcset = img.dataset.srcset;
          }
          
          img.classList.add('loaded');
          imageObserver.unobserve(img);
        }
      });
    });
    
    lazyImages.forEach(img => {
      imageObserver.observe(img);
    });
  } else {
    // Fallback for browsers without Intersection Observer support
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    lazyImages.forEach(img => {
      img.src = img.dataset.src;
      if (img.dataset.srcset) {
        img.srcset = img.dataset.srcset;
      }
      img.classList.add('loaded');
    });
  }
}

/**
 * Performance measurements (optional)
 * Can be used to track and improve site performance
 */
function measurePerformance() {
  if (window.performance && 'mark' in performance) {
    // Mark the end of critical content load
    performance.mark('criticalContentLoaded');
    
    // Measure time from navigation start to critical content load
    performance.measure('criticalTime', 'navigationStart', 'criticalContentLoaded');
    
    // Get the performance entries
    const perfEntries = performance.getEntriesByType('measure');
    
    perfEntries.forEach(entry => {
      if (entry.name === 'criticalTime') {
        console.log(`Critical content loaded in: ${Math.round(entry.duration)}ms`);
      }
    });
  }
}

/**
 * Newsletter form handling
 * Note: Most newsletter forms now use the Buttondown iframe embed
 */
function initNewsletterForm() {
  // This function is kept for backward compatibility
  // Modern newsletter forms use the Buttondown iframe embed
  console.log('Newsletter forms now use Buttondown iframe embedding');
  
  // Any remaining newsletter forms will still be handled here
  const newsletterForms = document.querySelectorAll('.newsletter-form');
  
  if (newsletterForms.length) {
    console.log(`Found ${newsletterForms.length} legacy newsletter forms`);
    // No need to add event listeners - these should be migrated to Buttondown iframes
  }
}

/**
 * Display a message after form submission
 */
function showFormMessage(form, message, type) {
  // Remove any existing message
  const existingMessage = form.querySelector('.form-message');
  if (existingMessage) {
    existingMessage.remove();
  }
  
  // Create new message element
  const messageElement = document.createElement('div');
  messageElement.className = `form-message ${type}`;
  messageElement.textContent = message;
  
  // Insert after the form
  form.insertAdjacentElement('afterend', messageElement);
  
  // Auto-remove after 5 seconds for success messages
  if (type === 'success') {
    setTimeout(() => {
      messageElement.classList.add('fade-out');
      setTimeout(() => messageElement.remove(), 500);
    }, 5000);
  }
}

/**
 * Initialize Bitcoin Report - Fetch and display real-time Bitcoin data
 */
function initBitcoinReport() {
  const bitcoinReport = document.getElementById('bitcoin-report');
  if (!bitcoinReport) return;
  
  // Elements to update
  const priceElement = document.getElementById('bitcoin-price');
  const changeElement = document.getElementById('bitcoin-change');
  const updateTimeElement = document.getElementById('bitcoin-update-time');
  const marketCapElement = document.getElementById('bitcoin-market-cap');
  const volumeElement = document.getElementById('bitcoin-volume');
  const dominanceElement = document.getElementById('bitcoin-dominance');
  const trendElement = document.getElementById('bitcoin-trend');
  const insightsList = document.getElementById('bitcoin-insights-list');
  
  // Function to fetch Bitcoin data
  async function fetchBitcoinData() {
    try {
      const response = await fetch('https://michaelditter.com/bitcoin-research-api/api/bitcoin-data');
      
      if (!response.ok) {
        throw new Error(`Error fetching Bitcoin data: ${response.status}`);
      }
      
      const data = await response.json();
      
      // Update UI with the data
      if (priceElement) priceElement.textContent = data.bitcoinPrice.current;
      if (changeElement) {
        changeElement.textContent = data.bitcoinPrice.weeklyChange;
        // Add appropriate class based on trend
        changeElement.className = 'btc-change ' + (data.bitcoinPrice.weeklyTrend === 'up' ? 'positive' : 'negative');
      }
      
      if (marketCapElement) marketCapElement.textContent = data.marketSummary.marketCap;
      if (volumeElement) volumeElement.textContent = data.marketSummary.volume24h;
      if (dominanceElement) dominanceElement.textContent = data.marketSummary.dominance;
      if (trendElement) {
        trendElement.textContent = data.bitcoinPrice.weeklyTrend === 'up' ? 'Bullish' : 'Bearish';
        trendElement.className = 'detail-value ' + (data.bitcoinPrice.weeklyTrend === 'up' ? 'positive' : 'negative');
      }
      
      // Update insights list
      if (insightsList) {
        insightsList.innerHTML = '';
        data.keyInsights.forEach(insight => {
          const li = document.createElement('li');
          li.innerHTML = `<strong>${insight.title}</strong>: ${insight.content.substring(0, 100)}...`;
          insightsList.appendChild(li);
        });
      }
      
      // Update the time
      if (updateTimeElement) {
        const now = new Date();
        updateTimeElement.textContent = `Updated: ${now.toLocaleDateString()} ${now.toLocaleTimeString()}`;
      }
      
    } catch (error) {
      console.error('Error fetching Bitcoin data:', error);
      
      // Display fallback data if fetch fails
      if (priceElement) priceElement.textContent = '$84,570';
      if (changeElement) {
        changeElement.textContent = '(+3.60%)';
        changeElement.className = 'btc-change positive';
      }
      if (updateTimeElement) updateTimeElement.textContent = 'Last updated: Today';
      if (marketCapElement) marketCapElement.textContent = '$1.65 trillion';
      if (volumeElement) volumeElement.textContent = '$48 billion';
      if (dominanceElement) dominanceElement.textContent = '52.1%';
      if (trendElement) {
        trendElement.textContent = 'Bullish';
        trendElement.className = 'detail-value positive';
      }
      
      // Fallback insights
      if (insightsList) {
        insightsList.innerHTML = `
          <li><strong>Institutional Adoption</strong>: Major financial institutions increasing their Bitcoin holdings...</li>
          <li><strong>ETF Decision Pending</strong>: The SEC is expected to announce decisions on several Bitcoin ETF applications...</li>
        `;
      }
    }
  }
  
  // Initial fetch
  fetchBitcoinData();
  
  // Refresh every 5 minutes
  setInterval(fetchBitcoinData, 5 * 60 * 1000);
}

/**
 * Initialize AI Report Section - Simple static display
 */
function initAIReportSection() {
  const aiReport = document.getElementById('ai-report');
  if (!aiReport) return;
  
  console.log('AI Report section initialized with static image');
  
  // Add any additional initialization if needed later
  // But for now, we're using static images instead of Chart.js
} 