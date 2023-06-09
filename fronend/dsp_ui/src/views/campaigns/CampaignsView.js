import { Table, TableBody, TableCell, TableHead, TableRow } from '@mui/material';
import React, {useState, Fragment} from 'react';
import EditableRow from './EditableRow';
import data from "./moch-data.json"
import ReadOnlyRow from './ReadOnlyRow';

function CampaignsView() {
    const [tableData, setTableData] = useState(data)
    const [editDataId, setEditDataId] = useState(null)
    const [editFormData, setEditFormData] = useState(
      {
        name: "",
        budget: 0,
        bidfloor: 0 
      }
    )
    
    const handleEditFormChange = (event) => {
        const fieldName = event.target.getAttribute('name');
        const fieldValue = event.target.value;

        const newFormData = { ...editFormData };
        newFormData[fieldName] = fieldValue;
        setEditFormData(newFormData);
    }

    const handleEditFormSubmit = (event) => {
      event.preventDefault()
      const editedContact = {
        id: editDataId,
        name: editFormData.name,
        budget: editFormData.budget,
        bidfloor: editFormData.bidfloor
      }
      const newContacs = [...tableData]
      const index = tableData.findIndex((obj) => obj.id === editDataId)
      
      newContacs[index] = editedContact
      setTableData(newContacs)
      setEditDataId(null)
    }

    const handleEditClick = (event, obj) => {
      event.preventDefault();
      setEditDataId(obj.id);

      const formValues = {
        name: obj.name,
        budget: obj.budget,
        bidfloor: obj.bidfloor
      }

      setEditFormData(formValues)
    }

    const handleCancelClick = () => {
      setEditDataId(null)
    }

    const handleDeleteClick = (objId) => {
      const newContacs = [...tableData]
      const index = tableData.findIndex((obj) => obj.id === objId)
      
      newContacs.splice(index, 1)
      setTableData(newContacs)
    }

    return <div className='campaigns-view'>
      <form onSubmit={handleEditFormSubmit}>
        <Table>
            <TableHead >
                <TableRow >
                    <TableCell>Name</TableCell>
                    <TableCell>Budget</TableCell>
                    <TableCell>Bid floor</TableCell>
                    <TableCell>Actions</TableCell>
                </TableRow>
            </TableHead>
            <TableBody>
                {tableData.map((obj)=> (
                  <Fragment>
                    {editDataId === obj.id ? (
                      <EditableRow 
                          editFormData={ editFormData }
                          handleEditFormChange={ handleEditFormChange }
                          handleCancelClick={handleCancelClick}
                          />
                    ): (
                      <ReadOnlyRow 
                          obj={obj}
                          handleObjectClick={handleEditClick}
                          handleDeleteClick={handleDeleteClick}/>
                    )}  
                  </Fragment>
                ))}
            </TableBody>
        </Table>
      </form>
    </div>
}

export default CampaignsView