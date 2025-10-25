import React from 'react'
import styles from "./Footer.module.css"
import { Link } from 'react-router-dom'

const Footer = () => {
  return (
    <>

    <footer className={styles.footer}>
        <div className={styles.container}>

            <div className={styles.aboutContent}>
                <h2>About Company</h2>
                <ul>
                    <li><Link to="">Our Story</Link></li>
                    <li><Link to="">Careers</Link></li>
                    <li><Link to="">Press & News</Link></li>
                    <li><Link to="">Sustainability</Link></li>
                </ul>
            </div>

    
            <div className={styles.helpContent}>
                <h2>Help Connections</h2>
                <ul>
                    <li><Link to="">FAQ</Link></li>
                    <li><Link to="">Shipping & Delivery</Link></li>
                    <li><Link to="">Returns & Exchanges</Link></li>
                    <li><Link to="">Contact Us</Link></li>
                </ul>
            </div>

        
            <div className={styles.socialsContent}>
                <h2>Social Links</h2>
                <ul>
                    <li><Link to=""><img src="" alt="" /></Link></li>
                    <li><Link to=""><img src="" alt="" /></Link></li>
                    <li><Link to=""><img src="" alt="" /></Link></li>
                    <li><Link to=""><img src="" alt="" /></Link></li>
                </ul>
            </div>
        </div>
    </footer>

    </>
  )
}

export default Footer
