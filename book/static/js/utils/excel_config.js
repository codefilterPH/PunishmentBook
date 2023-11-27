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
async function customizeWorksheet(xlsx, templatePath, data) {
    try {
        console.log('Begin downloading excel file.');

        // Fetch the template workbook
        const response = await fetch(templatePath);

        if (!response.ok) {
            throw new Error('Failed to fetch the template Excel file.');
        }

        const arrayBuffer = await response.arrayBuffer();
        const dataUint8Array = new Uint8Array(arrayBuffer);

        // Read the template workbook
        const templateWorkbook = XLSX.read(dataUint8Array, { type: 'array' });

        // Your customization logic here...
        const sheetName = templateWorkbook.SheetNames[0];
        const sheet = templateWorkbook.Sheets[sheetName];

        // Check if the sheet has a valid range
        if (!sheet['!ref']) {
            // Handle the case where the range is not defined
            sheet['!ref'] = 'A1:Z10'; // Set a default range that fits your data
        }

        const lastDataRowIndex = XLSX.utils.decode_range(sheet['!ref']).e.r;

        // Append DataTable data
        const dataTableRows = data.map(item => [item.personnel, item.offense, item.entry_date, item.actions]);
        XLSX.utils.sheet_add_aoa(sheet, dataTableRows, { origin: -1 });

        // Append remarks below the DataTable data
        const remarksRow = lastDataRowIndex + 2;
        const remarks = ['------------\nRemarks'];
        XLSX.utils.sheet_add_aoa(sheet, [remarks], { origin: { r: remarksRow, c: 0 } });

        // Append "approved by" below the remarks
        const approvedByRow = lastDataRowIndex + 4;
        const approver = ['------------\nApproved by'];
        XLSX.utils.sheet_add_aoa(sheet, [approver], { origin: { r: approvedByRow, c: 0 } });

        // Convert the modified workbook back to a binary string
        const modifiedBinaryString = XLSX.write(templateWorkbook, { bookType: 'xlsx', mimeType: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', type: 'binary' });

        // Convert the binary string to a Blob
        const blob = new Blob([s2ab(modifiedBinaryString)], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });

        // Save the blob to a file using FileSaver.js
        saveAs(blob, 'excel.xlsx');

        console.log('Customization successful');
    } catch (error) {
        console.error('An error occurred during customization:', error);
    }
}

// Helper function to convert a string to an ArrayBuffer
function s2ab(s) {
    const buf = new ArrayBuffer(s.length);
    const view = new Uint8Array(buf);
    for (let i = 0; i < s.length; i++) view[i] = s.charCodeAt(i) & 0xFF;
    return buf;
}