import React from "react";
import { TextField } from "@mui/material";
import Button from "@mui/material/Button";
import CampaingsView from "./CampaignsView"
import Typography from "@mui/material/Typography";
import Stack from "@mui/material/Stack";

function Campaigns() {
  return (
    <div className="Campaigns">
        <Stack 
            direction="row" 
            marginLeft={ 8 }
            marginTop={ 2 }
            marginRight={ 8 }
            marginBottom={ 4 }
            justifyContent="space-between"
            >
            <Typography component="h1" variant="h5">
                Campaigns
            </Typography>
            <Button>Create</Button>    
        </Stack>        
            
        <CampaingsView/>
    </div>
  );
}

export default Campaigns;
