


export function get_server(){
    return "http://localhost:5000";
}

export function is_up(){
    return fetch("http://localhost:5000/")
    .then(response => response.status===200);
}

export function get_data(){
    return fetch("http://localhost:5000/")
    .then(response => response.json());
}