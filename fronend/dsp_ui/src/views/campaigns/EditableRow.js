import { Input, TableRow, TableCell, Button } from '@mui/material'

import React, { Fragment } from 'react'

function EditableRow({editFormData, handleEditFormChange, handleCancelClick}) {
  return (
    <TableRow>
        <TableCell>
            <Input type='text' 
                   required='required'
                   placeholder='Enter name ...' 
                   name='name'
                   value={editFormData.name}
                   onChange={handleEditFormChange}>
            </Input>
        </TableCell>
        <TableCell>
            <Input type='text' 
                   required='required'
                   placeholder='Enter budget ...' 
                   name='budget'
                   value={editFormData.budget}
                   onChange={handleEditFormChange}>
            </Input>
        </TableCell>
        <TableCell>
            <Input type='text' 
                   required='required'
                   placeholder='Enter Bid Floor ...' 
                   name='bidfloor'
                   value={editFormData.bidfloor}
                   onChange={handleEditFormChange}>
            </Input>
        </TableCell>
        <TableCell>
            <Button type='submit'>Save</Button>
            <Button type='button' onClick={handleCancelClick}>Cancel</Button>
        </TableCell>
    </TableRow>
  )
}

export default EditableRow