/* ========================================================
   ClinicCare - Client API & Dynamic UI Helpers
   ======================================================== */

const API_BASE = '/api';

// Toast Notification
function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const iconMap = {
    success: 'bi-check-circle-fill',
    error: 'bi-exclamation-triangle-fill',
    info: 'bi-info-circle-fill'
  };

  const toast = document.createElement('div');
  toast.className = `clinic-toast ${type}`;
  toast.innerHTML = `
    <i class="bi ${iconMap[type] || 'bi-info-circle-fill'} toast-icon"></i>
    <div style="flex: 1;">
      <div style="font-weight: 700; font-size: 0.85rem; text-transform: uppercase; color: #64748b;">${type}</div>
      <div style="font-weight: 500; font-size: 0.92rem; color: #1e293b;">${message}</div>
    </div>
    <button type="button" class="btn-close" style="font-size: 0.75rem;" onclick="this.parentElement.remove()"></button>
  `;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// Generate Initials
function getInitials(name) {
  if (!name) return 'U';
  const clean = name.replace(/^Dr\.\s+/i, '').trim();
  const parts = clean.split(' ');
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase();
  }
  return clean.substring(0, 2).toUpperCase();
}

// Specialization Badge Styler
function getSpecialtyBadge(specialty) {
  const s = (specialty || 'General Physician').toLowerCase();
  let cls = 'badge-default';
  let icon = 'bi-heart-pulse';

  if (s.includes('dentist')) {
    cls = 'badge-dentist';
    icon = 'bi-emoji-smile';
  } else if (s.includes('pediatric')) {
    cls = 'badge-pediatrician';
    icon = 'bi-balloon';
  } else if (s.includes('orthopedic')) {
    cls = 'badge-orthopedic';
    icon = 'bi-person-walking';
  } else if (s.includes('ent')) {
    cls = 'badge-ent';
    icon = 'bi-ear';
  } else if (s.includes('physician') || s.includes('medicine')) {
    cls = 'badge-physician';
    icon = 'bi-capsule';
  } else if (s.includes('skin') || s.includes('derma')) {
    cls = 'badge-pediatrician';
    icon = 'bi-droplet';
  } else if (s.includes('eye') || s.includes('ophthalm')) {
    cls = 'badge-dentist';
    icon = 'bi-eye';
  }

  return `<span class="badge-specialty ${cls}"><i class="bi ${icon}"></i> ${specialty || 'General'}</span>`;
}

// Format ISO date string into readable Date and Time
function formatDateTime(dateString) {
  if (!dateString) return '-';
  const d = new Date(dateString);
  if (isNaN(d.getTime())) return dateString;
  const dateFormatted = d.toLocaleDateString(undefined, {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });
  const timeFormatted = d.toLocaleTimeString(undefined, {
    hour: '2-digit',
    minute: '2-digit'
  });
  return `<span class="fw-semibold">${dateFormatted}</span> <span class="text-muted small">at ${timeFormatted}</span>`;
}

// Format ISO date string for datetime-local input
function formatForDateTimeInput(dateString) {
  if (!dateString) return '';
  const d = new Date(dateString);
  if (isNaN(d.getTime())) return '';
  const pad = (n) => String(n).padStart(2, '0');
  const year = d.getFullYear();
  const month = pad(d.getMonth() + 1);
  const day = pad(d.getDate());
  const hours = pad(d.getHours());
  const minutes = pad(d.getMinutes());
  return `${year}-${month}-${day}T${hours}:${minutes}`;
}

// Get Query Parameter by Name
function getQueryParam(name) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(name);
}

// Generic API Client
async function apiGet(endpoint) {
  const response = await fetch(`${API_BASE}${endpoint}`);
  if (!response.ok) {
    const err = await response.json().catch(() => ({ message: 'Request failed' }));
    throw new Error(err.message || `Error ${response.status}`);
  }
  return await response.json();
}

async function apiPost(endpoint, data) {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({ message: 'Save failed' }));
    throw new Error(err.message || `Error ${response.status}`);
  }
  return await response.json();
}

async function apiPut(endpoint, data) {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({ message: 'Update failed' }));
    throw new Error(err.message || `Error ${response.status}`);
  }
  return await response.json();
}

async function apiDelete(endpoint) {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    method: 'DELETE'
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({ message: 'Delete failed' }));
    throw new Error(err.message || `Error ${response.status}`);
  }
  return await response.json();
}
