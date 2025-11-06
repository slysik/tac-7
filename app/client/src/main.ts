import './style.css'
import { api } from './api/client'

// Global state

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
  initializeQueryInput();
  initializeFileUpload();
  initializeModal();
  initializeRandomQueryButton();
  initializeEnhancedDropZones();
  loadDatabaseSchema();
});

// Helper function to get download icon
function getDownloadIcon(): string {
  return '📊 CSV Export';
}

// Query Input Functionality
function initializeQueryInput() {
  const queryInput = document.getElementById('query-input') as HTMLTextAreaElement;
  const queryButton = document.getElementById('query-button') as HTMLButtonElement;
  
  // Debouncing state
  let isQueryInProgress = false;
  let debounceTimer: number | null = null;
  const DEBOUNCE_DELAY = 400; // 400ms debounce delay
  
  const executeQuery = async () => {
    const query = queryInput.value.trim();
    if (!query || isQueryInProgress) return;
    
    // Clear any pending debounce timer
    if (debounceTimer) {
      clearTimeout(debounceTimer);
      debounceTimer = null;
    }
    
    isQueryInProgress = true;
    // Ensure UI is disabled (might already be disabled from click handler)
    queryButton.disabled = true;
    queryInput.disabled = true;
    queryButton.innerHTML = '<span class="loading"></span>';
    
    try {
      const response = await api.processQuery({
        query,
        llm_provider: 'openai'  // Default to OpenAI
      });
      
      displayResults(response, query);
      
      // Clear the input field on success
      queryInput.value = '';
    } catch (error) {
      displayError(error instanceof Error ? error.message : 'Query failed');
    } finally {
      isQueryInProgress = false;
      queryButton.disabled = false;
      queryInput.disabled = false;
      queryButton.textContent = 'Query';
    }
  };
  
  queryButton.addEventListener('click', () => {
    const query = queryInput.value.trim();
    if (!query || isQueryInProgress) return;
    
    // Debounce rapid clicks
    if (debounceTimer) {
      clearTimeout(debounceTimer);
    }
    
    // Immediately disable UI
    queryButton.disabled = true;
    queryInput.disabled = true;
    queryButton.innerHTML = '<span class="loading"></span>';
    
    debounceTimer = setTimeout(() => {
      executeQuery();
    }, DEBOUNCE_DELAY) as unknown as number;
  });
  
  // Allow Cmd+Enter (Mac) or Ctrl+Enter (Windows/Linux) to submit
  queryInput.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
      queryButton.click();
    }
  });
}

// Generate random query and populate input field
async function generateRandomQuery() {
  const queryInput = document.getElementById('query-input') as HTMLTextAreaElement;
  const generateButton = document.getElementById('generate-random-query-button') as HTMLButtonElement;

  // Only disable button if it exists (it may not exist in some contexts)
  const buttonExists = generateButton !== null;
  if (buttonExists) {
    generateButton.disabled = true;
    generateButton.innerHTML = '<span class="loading-secondary"></span>';
  }

  try {
    const response = await api.generateRandomQuery();

    // Always populate the query input field, even with error messages
    queryInput.value = response.query;
    queryInput.focus();

    if (response.error && response.error !== "No tables found in database") {
      // Only show errors for unexpected failures
      displayError(response.error);
    }
  } catch (error) {
    displayError(error instanceof Error ? error.message : 'Failed to generate random query');
  } finally {
    if (buttonExists) {
      generateButton.disabled = false;
      generateButton.textContent = 'Generate Random Query';
    }
  }
}

// Random Query Generation Functionality
function initializeRandomQueryButton() {
  const generateButton = document.getElementById('generate-random-query-button') as HTMLButtonElement;

  generateButton.addEventListener('click', async () => {
    await generateRandomQuery();
  });
}

// File Upload Functionality
function initializeFileUpload() {
  const dropZone = document.getElementById('drop-zone') as HTMLDivElement;
  const fileInput = document.getElementById('file-input') as HTMLInputElement;
  const browseButton = document.getElementById('browse-button') as HTMLButtonElement;
  
  // Browse button click
  browseButton.addEventListener('click', () => fileInput.click());
  
  // File input change
  fileInput.addEventListener('change', (e) => {
    const files = (e.target as HTMLInputElement).files;
    if (files && files.length > 0) {
      handleFileUpload(files[0]);
    }
  });
  
  // Drag and drop
  dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
  });
  
  dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
  });
  
  dropZone.addEventListener('drop', async (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    
    const files = e.dataTransfer?.files;
    if (files && files.length > 0) {
      handleFileUpload(files[0]);
    }
  });
}

// Handle file upload
async function handleFileUpload(file: File) {
  try {
    const response = await api.uploadFile(file);

    if (response.error) {
      displayError(response.error);
    } else {
      displayUploadSuccess(response);
      await loadDatabaseSchema();
    }
  } catch (error) {
    displayError(error instanceof Error ? error.message : 'Upload failed');
  }
}

// Enhanced Drop Zones - Helper Functions
function showDropOverlay(element: HTMLElement): HTMLElement {
  const overlay = document.createElement('div');
  overlay.className = 'drop-message';

  const text = document.createElement('div');
  text.className = 'drop-message-text';
  text.textContent = 'Drop to create table';

  overlay.appendChild(text);
  element.appendChild(overlay);

  return overlay;
}

function hideDropOverlay(element: HTMLElement): void {
  const overlay = element.querySelector('.drop-message');
  if (overlay) {
    overlay.remove();
  }
}

function isValidFileType(file: File): boolean {
  const validExtensions = ['.csv', '.json', '.jsonl'];
  const fileName = file.name.toLowerCase();
  return validExtensions.some(ext => fileName.endsWith(ext));
}

function hasFiles(dataTransfer: DataTransfer | null): boolean {
  if (!dataTransfer) return false;
  return Array.from(dataTransfer.types).includes('Files');
}

// Initialize Enhanced Drop Zones
function initializeEnhancedDropZones() {
  const querySection = document.getElementById('query-section') as HTMLElement;
  const tablesSection = document.getElementById('tables-section') as HTMLElement;

  // Setup drop zone for query section
  if (querySection) {
    setupDropZone(querySection);
  }

  // Setup drop zone for tables section
  if (tablesSection) {
    setupDropZone(tablesSection);
  }

  function setupDropZone(element: HTMLElement) {
    let localDragCounter = 0;

    element.addEventListener('dragenter', (e) => {
      e.preventDefault();
      const dataTransfer = (e as DragEvent).dataTransfer;

      if (hasFiles(dataTransfer)) {
        localDragCounter++;
        if (localDragCounter === 1) {
          element.classList.add('dragover');
          showDropOverlay(element);
        }
      }
    });

    element.addEventListener('dragover', (e) => {
      e.preventDefault();
      const dataTransfer = (e as DragEvent).dataTransfer;

      if (hasFiles(dataTransfer) && dataTransfer) {
        dataTransfer.dropEffect = 'copy';
      }
    });

    element.addEventListener('dragleave', (e) => {
      e.preventDefault();
      localDragCounter--;

      if (localDragCounter === 0) {
        element.classList.remove('dragover');
        hideDropOverlay(element);
      }
    });

    element.addEventListener('drop', async (e) => {
      e.preventDefault();
      e.stopPropagation();

      localDragCounter = 0;
      element.classList.remove('dragover');
      hideDropOverlay(element);

      const dataTransfer = (e as DragEvent).dataTransfer;
      const files = dataTransfer?.files;

      if (files && files.length > 0) {
        const file = files[0];

        if (!isValidFileType(file)) {
          displayError('Invalid file type. Please upload a .csv, .json, or .jsonl file.');
          return;
        }

        await handleFileUpload(file);
      }
    });
  }
}

// Load database schema
async function loadDatabaseSchema() {
  try {
    const response = await api.getSchema();
    if (!response.error) {
      displayTables(response.tables);
    }
  } catch (error) {
    console.error('Failed to load schema:', error);
  }
}

// Display query results
function displayResults(response: QueryResponse, query: string) {
  
  const resultsSection = document.getElementById('results-section') as HTMLElement;
  const sqlDisplay = document.getElementById('sql-display') as HTMLDivElement;
  const resultsContainer = document.getElementById('results-container') as HTMLDivElement;
  
  resultsSection.style.display = 'block';
  
  // Display natural language query and SQL
  sqlDisplay.innerHTML = `
    <div class="query-display">
      <strong>Query:</strong> ${query}
    </div>
    <div class="sql-query">
      <strong>SQL:</strong> <code>${response.sql}</code>
    </div>
  `;
  
  // Display results table
  if (response.error) {
    resultsContainer.innerHTML = `<div class="error-message">${response.error}</div>`;
  } else if (response.results.length === 0) {
    resultsContainer.innerHTML = '<p>No results found.</p>';
  } else {
    const table = createResultsTable(response.results, response.columns);
    resultsContainer.innerHTML = '';
    resultsContainer.appendChild(table);
  }
  
  // Initialize toggle button
  const toggleButton = document.getElementById('toggle-results') as HTMLButtonElement;
  toggleButton.addEventListener('click', () => {
    resultsContainer.style.display = resultsContainer.style.display === 'none' ? 'block' : 'none';
    toggleButton.textContent = resultsContainer.style.display === 'none' ? 'Show' : 'Hide';
  });
  
  // Add export button if results exist
  if (!response.error && response.results.length > 0) {
    const resultsHeader = document.querySelector('.results-header') as HTMLElement;
    
    // Remove existing button container if any
    const existingButtonContainer = resultsHeader.querySelector('.results-header-buttons');
    if (existingButtonContainer) {
      existingButtonContainer.remove();
    }
    
    // Create button container
    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'results-header-buttons';
    
    // Create export button
    const exportButton = document.createElement('button');
    exportButton.className = 'export-button secondary-button';
    exportButton.innerHTML = getDownloadIcon();
    exportButton.title = 'Export results as CSV';
    exportButton.onclick = async () => {
      try {
        await api.exportQueryResults(response.results, response.columns);
      } catch (error) {
        displayError('Failed to export results');
      }
    };
    
    // Remove toggle button from its current position
    toggleButton.remove();
    
    // Add buttons to container
    buttonContainer.appendChild(exportButton);
    buttonContainer.appendChild(toggleButton);
    
    // Add container to results header
    resultsHeader.appendChild(buttonContainer);
  }
}

// Create results table
function createResultsTable(results: Record<string, any>[], columns: string[]): HTMLTableElement {
  const table = document.createElement('table');
  table.className = 'results-table';
  
  // Header
  const thead = document.createElement('thead');
  const headerRow = document.createElement('tr');
  columns.forEach(col => {
    const th = document.createElement('th');
    th.textContent = col;
    headerRow.appendChild(th);
  });
  thead.appendChild(headerRow);
  table.appendChild(thead);
  
  // Body
  const tbody = document.createElement('tbody');
  results.forEach(row => {
    const tr = document.createElement('tr');
    columns.forEach(col => {
      const td = document.createElement('td');
      td.textContent = row[col] !== null ? String(row[col]) : '';
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);
  
  return table;
}

// Display tables
// Handle data generation for a table
async function handleGenerateData(tableName: string, button: HTMLButtonElement) {
  // Disable button and show loading state
  button.disabled = true;
  button.innerHTML = '<span class="loading"></span>';
  button.title = 'Generating data...';

  try {
    const response = await api.generateTableData(tableName);

    if (response.error) {
      displayError(`Failed to generate data: ${response.error}`);
    } else {
      displaySuccess(`Generated ${response.rows_added} rows for table '${response.table_name}'. New total: ${response.new_row_count} rows.`);
      // Reload database schema to update table row counts
      await loadDatabaseSchema();
      // Generate a sample query to help user explore the newly populated data
      await generateRandomQuery();
    }
  } catch (error) {
    displayError(`Failed to generate data: ${error}`);
  } finally {
    // Re-enable button and restore original state
    button.disabled = false;
    button.innerHTML = '⚡ Generate';
    button.title = 'Generate synthetic data using AI';
  }
}

function displayTables(tables: TableSchema[]) {
  const tablesList = document.getElementById('tables-list') as HTMLDivElement;

  if (tables.length === 0) {
    tablesList.innerHTML = '<p class="no-tables">No tables loaded. Upload data or use sample data to get started.</p>';
    return;
  }

  tablesList.innerHTML = '';

  tables.forEach(table => {
    const tableItem = document.createElement('div');
    tableItem.className = 'table-item';

    // Header section
    const tableHeader = document.createElement('div');
    tableHeader.className = 'table-header';

    const tableLeft = document.createElement('div');
    tableLeft.style.display = 'flex';
    tableLeft.style.alignItems = 'center';
    tableLeft.style.gap = '1rem';

    const tableName = document.createElement('div');
    tableName.className = 'table-name';
    tableName.textContent = table.name;

    const tableInfo = document.createElement('div');
    tableInfo.className = 'table-info';
    tableInfo.textContent = `${table.row_count} rows, ${table.columns.length} columns`;

    tableLeft.appendChild(tableName);
    tableLeft.appendChild(tableInfo);

    // Create buttons container
    const buttonsContainer = document.createElement('div');
    buttonsContainer.style.display = 'flex';
    buttonsContainer.style.gap = '0.5rem';
    buttonsContainer.style.alignItems = 'center';

    // Create generate data button
    const generateButton = document.createElement('button');
    generateButton.className = 'generate-data-button';
    generateButton.innerHTML = '⚡ Generate';
    generateButton.title = 'Generate synthetic data using AI';
    generateButton.onclick = async () => {
      await handleGenerateData(table.name, generateButton);
    };

    // Create export button
    const exportButton = document.createElement('button');
    exportButton.className = 'export-button table-export-button';
    exportButton.innerHTML = getDownloadIcon();
    exportButton.title = 'Export table as CSV';
    exportButton.onclick = async () => {
      try {
        await api.exportTable(table.name);
      } catch (error) {
        displayError('Failed to export table');
      }
    };

    const removeButton = document.createElement('button');
    removeButton.className = 'remove-table-button';
    removeButton.innerHTML = '&times;';
    removeButton.title = 'Remove table';
    removeButton.onclick = () => removeTable(table.name);

    buttonsContainer.appendChild(generateButton);
    buttonsContainer.appendChild(exportButton);
    buttonsContainer.appendChild(removeButton);

    tableHeader.appendChild(tableLeft);
    tableHeader.appendChild(buttonsContainer);

    // Columns section
    const tableColumns = document.createElement('div');
    tableColumns.className = 'table-columns';

    table.columns.forEach(column => {
      const columnTag = document.createElement('span');
      columnTag.className = 'column-tag';

      const columnName = document.createElement('span');
      columnName.className = 'column-name';
      columnName.textContent = column.name;

      const columnType = document.createElement('span');
      columnType.className = 'column-type';
      const typeEmoji = getTypeEmoji(column.type);
      columnType.textContent = `${typeEmoji} ${column.type}`;

      columnTag.appendChild(columnName);
      columnTag.appendChild(columnType);
      tableColumns.appendChild(columnTag);
    });

    tableItem.appendChild(tableHeader);
    tableItem.appendChild(tableColumns);
    tablesList.appendChild(tableItem);
  });
}

// Display upload success
function displayUploadSuccess(response: FileUploadResponse) {
  // Close modal
  const modal = document.getElementById('upload-modal') as HTMLElement;
  modal.style.display = 'none';
  
  // Show success message
  const successDiv = document.createElement('div');
  successDiv.className = 'success-message';
  successDiv.textContent = `Table "${response.table_name}" created successfully with ${response.row_count} rows!`;
  successDiv.style.cssText = `
    background: rgba(40, 167, 69, 0.1);
    border: 1px solid var(--success-color);
    color: var(--success-color);
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
  `;
  
  const tablesSection = document.getElementById('tables-section') as HTMLElement;
  tablesSection.insertBefore(successDiv, tablesSection.firstChild);
  
  // Remove success message after 3 seconds
  setTimeout(() => {
    successDiv.remove();
  }, 3000);
}

// Display error
function displayError(message: string) {
  const errorDiv = document.createElement('div');
  errorDiv.className = 'error-message';
  errorDiv.textContent = message;

  const resultsContainer = document.getElementById('results-container') as HTMLDivElement;
  resultsContainer.innerHTML = '';
  resultsContainer.appendChild(errorDiv);

  const resultsSection = document.getElementById('results-section') as HTMLElement;
  resultsSection.style.display = 'block';
}

// Display success message
function displaySuccess(message: string) {
  const successDiv = document.createElement('div');
  successDiv.className = 'success-message';
  successDiv.textContent = message;
  successDiv.style.cssText = `
    background: rgba(40, 167, 69, 0.1);
    border: 1px solid var(--success-color);
    color: var(--success-color);
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
  `;

  const tablesSection = document.getElementById('tables-section') as HTMLElement;
  tablesSection.insertBefore(successDiv, tablesSection.firstChild);

  // Remove success message after 3 seconds
  setTimeout(() => {
    successDiv.remove();
  }, 3000);
}

// Initialize modal
function initializeModal() {
  const uploadButton = document.getElementById('upload-data-button') as HTMLButtonElement;
  const modal = document.getElementById('upload-modal') as HTMLElement;
  const closeButton = modal.querySelector('.close-modal') as HTMLButtonElement;
  
  // Open modal
  uploadButton.addEventListener('click', () => {
    modal.style.display = 'flex';
  });
  
  // Close modal
  closeButton.addEventListener('click', () => {
    modal.style.display = 'none';
  });
  
  // Close on background click
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.style.display = 'none';
    }
  });
  
  // Initialize sample data buttons
  const sampleButtons = modal.querySelectorAll('.sample-button');
  sampleButtons.forEach(button => {
    button.addEventListener('click', async (e) => {
      const sampleType = (e.currentTarget as HTMLElement).dataset.sample;
      await loadSampleData(sampleType!);
    });
  });
}

// Remove table
async function removeTable(tableName: string) {
  if (!confirm(`Are you sure you want to remove the table "${tableName}"?`)) {
    return;
  }
  
  try {
    const response = await fetch(`/api/table/${tableName}`, {
      method: 'DELETE'
    });
    
    if (!response.ok) {
      throw new Error('Failed to remove table');
    }
    
    // Reload schema
    await loadDatabaseSchema();
    
    // Show success message
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = `Table "${tableName}" removed successfully!`;
    successDiv.style.cssText = `
      background: rgba(40, 167, 69, 0.1);
      border: 1px solid var(--success-color);
      color: var(--success-color);
      padding: 1rem;
      border-radius: 8px;
      margin-bottom: 1rem;
    `;
    
    const tablesSection = document.getElementById('tables-section') as HTMLElement;
    tablesSection.insertBefore(successDiv, tablesSection.firstChild);
    
    setTimeout(() => {
      successDiv.remove();
    }, 3000);
  } catch (error) {
    displayError(error instanceof Error ? error.message : 'Failed to remove table');
  }
}

// Get emoji for data type
function getTypeEmoji(type: string): string {
  const upperType = type.toUpperCase();
  
  // SQLite types
  if (upperType.includes('INT')) return '🔢';
  if (upperType.includes('REAL') || upperType.includes('FLOAT') || upperType.includes('DOUBLE')) return '💯';
  if (upperType.includes('TEXT') || upperType.includes('CHAR') || upperType.includes('STRING')) return '📝';
  if (upperType.includes('DATE') || upperType.includes('TIME')) return '📅';
  if (upperType.includes('BOOL')) return '✓';
  if (upperType.includes('BLOB')) return '📦';
  
  // Default
  return '📊';
}

// Load sample data
async function loadSampleData(sampleType: string) {
  try {
    let filename: string;
    
    if (sampleType === 'users') {
      filename = 'users.json';
    } else if (sampleType === 'products') {
      filename = 'products.csv';
    } else if (sampleType === 'events') {
      filename = 'events.jsonl';
    } else {
      throw new Error(`Unknown sample type: ${sampleType}`);
    }
    
    const response = await fetch(`/sample-data/${filename}`);
    
    if (!response.ok) {
      throw new Error('Failed to load sample data');
    }
    
    const blob = await response.blob();
    const file = new File([blob], filename, { type: blob.type });
    
    // Upload the file
    await handleFileUpload(file);
  } catch (error) {
    displayError(error instanceof Error ? error.message : 'Failed to load sample data');
  }
}
