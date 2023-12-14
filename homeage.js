import React from "react";
import ResponsiveAppBar from "./dashboard";
import { Typography } from "@mui/material";
const Home =()=>{
    return(
        <div>
        <ResponsiveAppBar/>
        <Typography
  variant="h2"
  align="center"
  sx={{
    fontWeight: 'bold',
    color: 'white',
    paddingTop:'120px'
  }}
>
  Welcome to the class;)
</Typography>
        <Typography
  variant="h5"
  align="center"
  sx={{
    color: 'white',
  }}
>
  No.on.roll:
</Typography>
        <Typography
  variant="h5"
  align="center"
  sx={{
    color: 'white',
  }}
>
  No.of.present:
</Typography>

        </div>
    );
}; 
export default Home;
