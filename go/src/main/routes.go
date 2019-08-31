package main

import "net/http"

func registerRoutes() {

	http.HandleFunc("/", readHandler)
	http.HandleFunc("/contacts/create", createHandler)
	http.HandleFunc("/contacts/list", readHandler)
	http.HandleFunc("/contacts/update", updateHandler)
	http.HandleFunc("/contacts/delete", deleteHandler)
	http.Handle("/static/",
		http.StripPrefix("/static/", http.FileServer(http.Dir("./statics"))),
	)
}
