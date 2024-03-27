import {useState} from "react"

const ContactForm = ({}) => {
    const [firstName, setFirstName] = useState("")
    const [lastName, setLastName] = useState("")
    const [email, setEmail] = useState("")
    const [phone, setPhone] = useState("")
    const [address, setAddress] = useState("")

    const onSubmit = async (e) => {
        // to prevent refreshing the page
        e.preventDefault()

        const data = {
            firstName,
            lastName,
            email,
            phone,
            address
        }
        const url = "http://127.0.0.1:5000/create_contact"
        const options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        }
        const response = await fetch(url, options)
        if (response.status !== 201 && response.status !== 200){
            const data = await response.json()
            alert(data.message)
        }
        else {
            // success!
        }
    }

    return 
    <form onSubmit={onSubmit}>
        <div>
            <label htmlFor="firstName">First Name:</label>
            <input type="text" id="firstName" value={firstName} onChange={(e) => setFirstName(e.target.value)} />
        </div>
        <div>
            <label htmlFor="lastName">Last Name:</label>
            <input type="text" id="lastName" value={lasttName} onChange={(e) => setLastName(e.target.value)} />
        </div>
        <div>
            <label htmlFor="email">Email:</label>
            <input type="text" id="email" value={email} onChange={(e) => setEmail(e.target.value)} />
        </div>
        <div>
            <label htmlFor="phone">Phone Number:</label>
            <input type="text" id="phone" value={phone} onChange={(e) => setPhone(e.target.value)} />
        </div>
        <div>
            <label htmlFor="address">Address:</label>
            <input type="text" id="address" value={address} onChange={(e) => setAddress(e.target.value)} />
        </div>
        <button type="submit">Add Contact</button>
    </form>
}

export default ContactForm