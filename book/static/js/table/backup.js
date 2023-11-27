/**
 * Customizes the Excel workbook by adding remarks and an "approved by" section before exporting.
 *
 * @param {Object} xlsx - The Excel workbook object.
 * @param {string} templatePath - The path to the Excel template file.
 * @param {Object[]} data - An array of data to be inserted into the sheet.
 * @throws {Error} Throws an error if an issue occurs during customization.
 * @description Reads the template file, modifies the sheet by adding remarks and an "approved by" section,
 * and triggers the download of the customized Excel file.
 */
function customizeWorksheet(xlsx, templatePath, data) {
    try {
        console.log('Begin downloading excel file.')
        var remarks = ['------------\nRemarks'];
        var approver = ['------------\nApproved by'];

        // Fetch the template workbook
        fetch(templatePath)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch the template Excel file.');
                }
                return response.arrayBuffer();
            })
            .then(templateData => {
                const arrayBuffer = templateData;
                const data = new Uint8Array(arrayBuffer);
                const modifiedWorkbook = XLSX.read(data, { type: 'array' });

                // Your customization logic here...
                const sheetName = modifiedWorkbook.SheetNames[0];
                const sheet = modifiedWorkbook.Sheets[sheetName];
                XLSX.utils.sheet_add_aoa(sheet, [remarks], { origin: -1 });
                XLSX.utils.sheet_add_aoa(sheet, [approver], { origin: -1 });

                // Convert the modified workbook back to a blob
                const blob = XLSX.write(modifiedWorkbook, { bookType: 'xlsx', type: 'blob' });

                // Save the blob to a file using FileSaver.js
                saveAs(blob, 'customized_excel_file.xlsx');

                console.log('Customization successful');
            })
            .catch(error => {
                console.error('An error occurred during customization:', error);
            });

        } catch (error) {
            console.error('An unexpected error occurred:', error);
        }
    }

/**
 * Initializes the DataTable for submitted violations.
 *
 * @param {Object} params - Parameters for customization.
 *   @property {string} params.excelUrl - The URL of the Excel template file.
 */
function initSubmittedViolationsDT(params) {
    var submittedViolation = $('#submittedViolationDt').DataTable({
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excel',
                text: 'Export to Excel',
                customize: function (xlsx) {
                    var templatePath = params.excelUrl; // Update with the correct path
                    // Extract filename from the URL
                    var filename = templatePath.split('/').pop();
                    console.log('Using template file:', filename);

                    var data = submittedViolation.ajax.json().data;

                    customizeWorksheet(xlsx, templatePath, data);
                }
            },
            {
                extend: 'csv',
                text: 'Export to CSV',
            },
            {
                extend: 'copy',
                text: 'Copy to Clipboard',
            },
            {
                extend: 'pdf',
                text: 'Export as PDF',
            }, 'print',
        ],
        serverSide: true,
        processing: true,
        ajax: {
            url: '/submitted-offense-dt/',
            type: 'GET',
        },
        columns: [
            { data: 'personnel' },
            { data: 'offense' },
            { data: 'entry_date' },
            { data: 'actions' }
        ],
        lengthMenu: [10, 25, 50, 100],
    });

    // Function to refresh the DataTable
    function fetchSubmittedOffense() {
        submittedViolation.ajax.reload();
    }

    // Trigger DataTable refresh when the button is clicked
    $('#btnRefresh').on('click', function () {
        fetchSubmittedOffense();
        console.log('clicked submitted violations');
    });
}
