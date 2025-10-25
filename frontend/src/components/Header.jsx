import React from 'react'
import { Link, useLocation } from 'react-router-dom';
import styles from "./Header.module.css"

const Header = () => {

    const location = useLocation();

    const links = [
        { name: 'Home', path: '/home' },
        { name: 'About', path: '/about' },
        { name: 'Contacts', path: '/contacts' },
        { name: 'Sign Up', path: '/sign-in' }
    ];


    return (
        <>
        <header className={styles.header}>
            <div className={styles.container}>
                <nav className={styles.nav}>
                    <ul>
                        {links.map(link => (
                            <li>
                                <Link to={link.path} className={location.pathname === link.path ? styles.activePage : styles.nonActive}>
                                    {link.name}
                                </Link>
                            </li>
                        ))}
                    </ul>
                </nav>

                <div className={styles.headerLogo}>
                    <img src="/headerLogo.svg" alt="" />
                </div>

            </div>

        </header>
        </>
    )
    }

export default Header
