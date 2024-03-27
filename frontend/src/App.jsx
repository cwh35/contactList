import { useState, useEffect } from 'react'
import ContactList from './ContactList'
import './App.css'

function App() {
  const [contacts, setContacts] = useState([{"firstName":"Cam","lastName":"Henning","email": "email", "phone": "1234567890", "address": "1234 Main St", id: 1}])

  useEffect(() => {
    //fetchContacts()
  }, [])

  const fetchContacts = async () => {
    // send request to the backend to get the contacts
    // use fetch to send a request
    const response = await fetch("http://127.0.0.1:5000/contacts")
    const data = await response.json()
    setContacts(data.contacts)
    console.log(data.contacts)
  }


  return <ContactList contacts={contacts} />
      
}

export default App
