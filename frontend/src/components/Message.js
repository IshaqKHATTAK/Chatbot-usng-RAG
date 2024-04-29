import React, { useState } from 'react';

export default function Message({ question }){
    return(
        <>
        <div className='container d-flex  justify-content-center' style={{width:'80%'}}>
            <p style={{background:'rgb(133, 193, 233)', marginLeft:0}} className='border border-2 border-primary rounded'>Question: {question}</p>
            {/* Render other messages here */}
        </div>
        </>
    )
}