import React from 'react'
import { TableRow, TableCell, Button } from '@mui/material'


function ReadOnlyRow({obj, handleObjectClick, handleDeleteClick}) {
  return (
    <TableRow>
        <TableCell>{obj.name}</TableCell>
        <TableCell>{obj.budget}</TableCell>
        <TableCell>{obj.bidfloor}</TableCell>
        <TableCell>
            <Button 
                type='button' 
                onClick={ (event) => handleObjectClick(event, obj) } >
                    Edit
            </Button>
            <Button
                type='button'
                onClick={() => handleDeleteClick(obj.id)}
                >
                Delete
            </Button>
        </TableCell>
    </TableRow>
        
  )
}

export default ReadOnlyRow