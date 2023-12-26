console.log('Hello world!')

const ws = new WebSocket('ws://localhost:8080')
const headers = ["Date", "Currency", "Sale", "Purchase"]

formChat.addEventListener('submit', (e) => {
    removeAllRows()
    deleteHeaders()
    createWaitMsgElement()
    e.preventDefault()
    ws.send(textField.value)
    textField.value = null
})

ws.onopen = (e) => {
    console.log('Hello WebSocket!')
}

// Function to create a table row and add it to the table body
function addRow(data) {
  const tableBody = document.getElementById('tableBody');
  const newRow = document.createElement('tr');

  data.forEach(item => {
    const cell = document.createElement('td');
    cell.textContent = item;
    newRow.appendChild(cell);
  });

  tableBody.appendChild(newRow);
}

// Function to remove all rows from the table
function removeAllRows() {
  const tableBody = document.getElementById('tableBody');

  // Remove all rows in the table body
  while (tableBody.firstChild) {
    tableBody.removeChild(tableBody.firstChild);
  }
}

// Function to remove all headers from the table
function deleteHeaders() {
  const tableHead = document.getElementById('tableHead');

  // Remove all headers in the thead
    if (tableHead){
        while (tableHead.firstChild) {
            tableHead.removeChild(tableHead.firstChild);
        }
    }
}

// Function to create table headers dynamically
function createHeaders(headers) {
  const tableHead = document.getElementById('tableHead');
  const headerRow = document.createElement('tr');

  headers.forEach(headerText => {
    const headerCell = document.createElement('th');
    headerCell.textContent = headerText;
    headerRow.appendChild(headerCell);
  });

  tableHead.appendChild(headerRow);
}

function createWaitMsgElement(){
    const elMsg = document.createElement('div')
    elMsg.textContent = "Wait for the exchange rates"
    const subscribe = document.getElementById("subscribe")
    subscribe.appendChild(elMsg)
}

function createErrorMsgElement(msg){
    const elMsg = document.createElement('div')
    elMsg.textContent = msg
    const subscribe = document.getElementById("subscribe")
    subscribe.appendChild(elMsg)
}

function removeWaitMsgElement(){
    const subscribe = document.getElementById("subscribe");
    while (subscribe.firstChild) {
        subscribe.removeChild(subscribe.firstChild);
    }
}

ws.onmessage = (e) => {
    console.log(typeof e.data)
    console.log(e.data)
    // Remove wait message
    removeWaitMsgElement()
    // Populate the table with the provided data
    try{
        const rates = JSON.parse(e.data)
        // Create headers
        createHeaders(headers)
        rates.forEach(rowData => {
            addRow(rowData);
        });
    }
    catch (error){
        createErrorMsgElement(e.data)
    }
}