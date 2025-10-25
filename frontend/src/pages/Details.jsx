import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import styles from "./Details.module.css"
import Footer from '../components/Footer'



const Details = (props) => {
    const [data, setData] = useState("");
    const [count, setCount] = useState(0);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null)
        
    useEffect(() => {
        const uploadData = async () => {
            try{
                const response = await fetch("https://www.crunchyroll.com/ru/discover?srsltid=AfmBOoocclsQtUWUkg2jWGYO12OWEDg8_ZTjE2gWvRo2CL-ag8zEJNTl");
            
                if (!response.ok){
                    throw new Error("error")
                }
                let result = await response.json();

                setTimeout(() => setData(result), 2000);
            }
            catch (error){
                setError(error)
            }
            finally{
                setLoading(false);
            }
        }
        uploadData()

    }, [count])


    const { products } = props;
    const { id } = useParams();

    const product = products.find(p => p.id === Number(id))
    if (!product){
        return (
            <div className={styles.errorMessage}>
                Product not found
            </div>
        )
    }




    return (
        <>
            <div className={styles.productDetail}>
                <h2>{product.name}</h2>
                <div className={styles.productDataContent}>
                    <p>Price: ${product.price}</p>
                    <p>Narrator: {product.narrator}</p>
                </div>
                <p>{count}</p>
                <button className={styles.button} onClick={()=>{setCount(count+1)}}>Add to Cart</button>
            </div>

            <div>
                { loading? <p>loading...</p> : <p>done</p>}
                {error && <p>{error}</p>}
            </div>
            <pre>{JSON.stringify(data, null, 2)}</pre>

            <Footer/>
        </>
    )
}

export default Details
