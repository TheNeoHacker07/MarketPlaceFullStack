import React from 'react'
import styles from "./Login.module.css"
import Footer from '../components/Footer'

const Login = ({login, setLogin}) => {
  return (
    <>    
    <div className={styles.form_box}>
        <form action="" onSubmit={(e) => {
                e.preventDefault();
                setLogin(login + "dfsd");
            }}>

            <h1>Enter your data</h1>

            <div className={styles.input_field}>
                <label htmlFor="">Username</label>
                <input type="text" className={styles.input_place} placeholder='enter username'/>
            </div>

            <div className={styles.input_field}>
                <label htmlFor="">Email</label>
                <input type="text" className={styles.input_place} placeholder='enter your email'/>
            </div>
            <div className={styles.input_field}>
                <label htmlFor="">Password</label>
                <input type="password" className={styles.input_place} placeholder='enter your password'/>
            </div>

            <div className={styles.input_field}>
                <label htmlFor="">Password Confirm</label>
                <input type="password" className={styles.input_place} placeholder='password confirm'/>
            </div>

            <button className={styles.submitButton} type='submit' >
                Sign Up
            </button>
        </form>
    </div>
    <Footer/>
    </>
  )
}

export default Login;
