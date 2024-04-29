import React, { useState } from 'react';

export default function InputBox({onSubmit}){
    const [message, setMessage] = useState('')
    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(message); // Pass the message to the onSubmit function
        setMessage(''); // Clear input field after submission
    };
    return(
        <>
        {/* onSubmit={handleSubmit} */}
        <div className="container" >
            <form className='d-flex align-items-center justify-content-center fixed-bottom mb-3' onSubmit={handleSubmit}>
                <input
                type='text'
                style={{width:"50%", height:"100px",  marginRight: "10px", marginTop:'6px'}}
                placeholder="Enter your message..."
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                />
                 <button type="submit" className="btn btn-outline-primary" style={{height:'100px',width:'80px'}}>Ask</button>
            </form>
        </div>
        </>
    )
}