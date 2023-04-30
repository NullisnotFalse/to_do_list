window.onload = () => {
    console.log("로딩되었음")
}

async function handleSignup() {
    const email = document.getElementById("email").value
    const password = document.getElementById("password").value
    const name = document.getElementById("name").value
    const gender = document.getElementById("gender").value
    const age = document.getElementById("age").value
    const introduction = document.getElementById("introduction").value
    console.log(email, password, name, gender, age, introduction)

    const response = await fetch('http://127.0.0.1:8000/users/signup/', {
        headers: {
            'content-type': 'application/json',
        },
        method: 'POST',
        body: JSON.stringify({
            "email": email,
            "password": password,
            "name": name,
            "gender": gender,
            "age": age,
            "introduction": introduction
        })
    })

    const response_json = await response.json()
    console.log(response_json)
}


async function handleLogin() {
    const email = document.getElementById("email").value
    const password = document.getElementById("password").value
    console.log(email, password)

    const response = await fetch('http://127.0.0.1:8000/users/api/token/', {
        headers: {
            'content-type': 'application/json',
        },
        method: 'POST',
        body: JSON.stringify({
            "email": email,
            "password": password,
        })
    })

    const response_json = await response.json()
    console.log(response_json)

    localStorage.setItem("access", response_json.access)
    localStorage.setItem("refresh", response_json.refresh)


    const base64Url = response_json.access.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    localStorage.setItem("payload", jsonPayload);

}



async function handleLogout() {
    localStorage.removeItem("access")
    localStorage.removeItem("refresh")
    localStorage.removeItem("payload")
}




// async function handleMock() {
//     const response = await fetch('http://127.0.0.1:8000/users/mock/', {
//         headers: {
//             "Authorization": "Bearer" + localStorage.getItem("access")
//         },
//         method: 'GET'
//     })
//     console.log(response)
// }


