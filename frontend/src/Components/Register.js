import React, { useState } from 'react';
import { Typography, Grid, TextField, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import axios from 'axios'

const Register = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    email: '',
    password: '',
  });

  const navigate = useNavigate();

  const handleSubmit = async(e) => {
    e.preventDefault();
    console.log('Registration Form Data:', formData);
    const result = await axios.post("http://127.0.0.1:8000/BookABook/register/",{
      "username": `${formData.firstName}`,
      "password": `${formData.password}`,
      "email": `${formData.email}`,
    }  
  )
  console.log(result)
  if(result?.status === 200){
    sessionStorage.setItem("user_id", result.data.userid);
    navigate('/user-setup')
  }
  };

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRedirect = () => {
    navigate('/login'); 
  };

  return (
    <div>
      <Typography variant="h4" gutterBottom>Register</Typography>
      <form onSubmit={handleSubmit}>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <TextField
              variant="outlined"
              required
              fullWidth
              id="firstName"
              label="First Name"
              name="firstName"
              value={formData.firstName}
              onChange={handleInputChange}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              variant="outlined"
              required
              fullWidth
              id="email"
              label="Email Address"
              name="email"
              autoComplete="email"
              value={formData.email}
              onChange={handleInputChange}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              variant="outlined"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="new-password"
              value={formData.password}
              onChange={handleInputChange}
            />
          </Grid>
        </Grid>
        <Button
          type="submit"
          fullWidth
          variant="contained"
          color="primary"
          sx={{ mt: 2 }}
        >
          Sign Up
        </Button>
      </form>

      <div>Or if you already have an account</div>
      <Button
        onClick={handleRedirect} 
        fullWidth
        variant="contained"
        color="primary"
        sx={{ mt: 2 }}
      >
        Login
      </Button>
      </div>
  );
};

export default Register;
