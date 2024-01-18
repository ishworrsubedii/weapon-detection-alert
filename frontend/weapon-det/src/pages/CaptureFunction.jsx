import React, { useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';

const columns = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'firstName', headerName: 'First name', width: 130 },
    { field: 'lastName', headerName: 'Last name', width: 130 },
    {
        field: 'age',
        headerName: 'Age',
        type: 'number',
        width: 90,
    },
    {
        field: 'fullName',
        headerName: 'Full name',
        description: 'This column has a value getter and is not sortable.',
        getCellProps: (params) => ({
            style: {
                color: '#fff', // Change 'white' to '#fff'
            },
        }),
        sortable: false,
        width: 160,
        valueGetter: (params) =>
            `${params.row.firstName || ''} ${params.row.lastName || ''}`,
    },
];

const rows = [
    { id: 1, lastName: 'Snow', firstName: 'Jon', age: 35 },
    { id: 2, lastName: 'Lannister', firstName: 'Cersei', age: 42 },
    { id: 3, lastName: 'Lannister', firstName: 'Jaime', age: 45 },
    { id: 4, lastName: 'Stark', firstName: 'Arya', age: 16 },
    { id: 5, lastName: 'Targaryen', firstName: 'Daenerys', age: null },
    { id: 6, lastName: 'Melisandre', firstName: null, age: 150 },
    { id: 7, lastName: 'Clifford', firstName: 'Ferrara', age: 44 },
    { id: 8, lastName: 'Frances', firstName: 'Rossini', age: 36 },
    { id: 9, lastName: 'Roxie', firstName: 'Harvey', age: 65 },
];
const CaptureImage = () => {
    const [isCapturing, setIsCapturing] = useState(false);

    const startCapture = () => {
        setIsCapturing(true);
        // Add your start capture logic here
    };

    const stopCapture = () => {
        setIsCapturing(false);
    };

    return (
        <>
            <div style={{
                width: '700px',
                height: '500px',
                position: 'absolute',
                left: '50%',
                top: '40%',
                transform: 'translate(-50%, -50%)',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                backgroundColor: '#f2f2f2',
                borderRadius: '10px',
                boxShadow: '0 0 10px rgba(0, 0, 0, 0.2)', // Optional: Add a subtle shadow
            }}>
            </div>
            <h2
                style={{
                    position: 'absolute',
                    left: '50%',
                    top: '6%',
                    transform: 'translate(-50%, -50%)',
                }}>Image Capture</h2>

            <div

                style={{
                    position: 'absolute',
                    left: '40%',
                    top: '70%',
                }}
            >
                <button onClick={startCapture} disabled={isCapturing}>Start Image Capturing</button>
                <button onClick={stopCapture} disabled={!isCapturing}>Stop Camera Capturing</button>

            </div>
            <div style={{
                position: 'absolute',
                top: '80%',
                left: '30%',
                color: 'white',
                textDecorationColor: 'white',
                height: 400, width: '50%'
            }}>
                <DataGrid
                    rows={rows}
                    columns={columns}
                    initialState={{
                        pagination: {
                            paginationModel: { page: 0, pageSize: 5 },
                        },
                    }}
                    pageSizeOptions={[5, 10]}
                    checkboxSelection
                />
            </div>
        </>
    );
};

export default CaptureImage;
