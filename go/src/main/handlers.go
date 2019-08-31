package main

import (
	"fmt"
	"html/template"
	"net/http"
	"strconv"
)

func createHandler(w http.ResponseWriter, r *http.Request) {

	listRedirect(w, r)

	var contact Contact
	contact.Username = r.FormValue("Username")
	contact.FirstName = r.FormValue("FirstName")
	contact.LastName = r.FormValue("LastName")
	contact.Email = r.FormValue("Email")
	fmt.Println(contact)

	stmt, err := db.Prepare("INSERT INTO contact(username, first_name, last_name, email) VALUES (?, ?, ?, ?)")
	panicIfNil(err, "Prepare query error")

	_, err = stmt.Exec(contact.Username, contact.FirstName, contact.LastName,  contact.Email)
	panicIfNil(err, "Execute query error")

	http.Redirect(w, r, "/contacts/list", 301)
}

func readHandler(w http.ResponseWriter, r *http.Request) {

	if r.Method != "GET" {
		http.Error(w, "Method not allowed", http.StatusBadRequest)
	}

	rows, err := db.Query("SELECT * FROM contact")
	checkInternalServerError(err, w)

	var contacts []Contact
	var contact Contact

	for rows.Next() {
		err = rows.Scan(&contact.Id, &contact.Username, &contact.FirstName, &contact.LastName, &contact.Email)
		checkInternalServerError(err, w)
		contacts = append(contacts, contact)
	}

	t, err := template.ParseFiles("tmpl/list.html")
	checkInternalServerError(err, w)

	err = t.Execute(w, contacts)
	checkInternalServerError(err, w)
}

func updateHandler(w http.ResponseWriter, r *http.Request) {

	listRedirect(w, r)

	var contact Contact
	contact.Id, _ = strconv.ParseInt(r.FormValue("Id"), 10, 64)
	contact.Username = r.FormValue("Username")
	contact.FirstName = r.FormValue("FirstName")
	contact.LastName = r.FormValue("LastName")
	contact.Email = r.FormValue("Email")
	fmt.Println(contact)

	stmt, err := db.Prepare("UPDATE contact SET username=?, first_name=?, last_name=?, email=? WHERE id=?")
	checkInternalServerError(err, w)
	fmt.Println(stmt)

	resp, err := stmt.Exec(contact.Username, contact.FirstName, contact.LastName, contact.Email, contact.Id)
	checkInternalServerError(err, w)

	_, err = resp.RowsAffected()
	checkInternalServerError(err, w)

	http.Redirect(w, r, "/contacts/list", 301)
}

func deleteHandler(w http.ResponseWriter, r *http.Request) {

	listRedirect(w, r)

	var costId, _ = strconv.ParseInt(r.FormValue("Id"), 10, 64)
	stmt, err := db.Prepare("DELETE FROM contact WHERE id=?")
	checkInternalServerError(err, w)
	fmt.Println(stmt)

	resp, err := stmt.Exec(costId)
	checkInternalServerError(err, w)

	_, err = resp.RowsAffected()
	checkInternalServerError(err, w)

	http.Redirect(w, r, "/contacts/list", 301)
}

func listRedirect(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		http.Redirect(w, r, "/contacts/list", 301)
	}
}