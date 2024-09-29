import React, { useState } from 'react';
import { Typography, Grid, TextField, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios'

const LoginPage = () => {
  const [username, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const history = useNavigate(); 
  const handleSubmit = async(e) => {
    e.preventDefault();
    console.log('Login Form Data:', { username, password });
    axios.post("http://127.0.0.1:8000/BookABook/login/", {
      "username": `${username}`,
	    "password": `${password}`

    }).then((result) => {
      console.log(result)
      history('/');

    })
  };

  const navigate = useNavigate();

  const handleRedirect = () => {
    navigate('/register'); 
  };
  return (
    <div>
      <Typography variant="h4" gutterBottom>Login</Typography>
      <form onSubmit={handleSubmit}>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <TextField
              variant="outlined"
              required
              fullWidth
              id="email"
              label="Email Address"
              name="email"
              autoComplete="email"
              value={username}
              onChange={(e) => setEmail(e.target.value)}
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
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
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
          Sign In
        </Button>
      </form>

      <div>Or if you don't have an account</div>
      <Button
        onClick={handleRedirect} 
        fullWidth
        variant="contained"
        color="primary"
        sx={{ mt: 2 }}
      >
        Sign Up
      </Button>
    </div>
  );
};

export default LoginPage;
