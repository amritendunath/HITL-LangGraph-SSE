import axios from 'axios'

const BASE_URL = process.env.BASE_URL

class assistantService {

    static async startConversation() {
        try {
            const response = await axios({
                url: `${BASE_URL}/graph/start`,
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            if (response.status >= 200 && response.status < 300) {
                return response.data
            }
            else {
                console.error("Server responded with error", response.status, response.data)
            }
        } catch (error) {
            console.log("Error starting conversations",error)
        }
    }

}

export default assistantService