package main

import (
	"database/sql"
	"net/http"

	_ "github.com/mattn/go-sqlite3"
)

var (
	db  *sql.DB
	err error
)

func main() {

	db, err = sql.Open("sqlite3", "de.sqlite3")
	panicIfNil(err, "Unable to establish sqlite connection.")
	stmt, _ := db.Prepare(`
		CREATE TABLE IF NOT EXISTS contact (id INTEGER PRIMARY KEY, username TEXT, first_name TEXT, last_name TEXT, email TEXT)
	`)
	_, err := stmt.Exec()
	panicIfNil(err, "Unable to create contact table.")

	defer db.Close()

	err = db.Ping()
	panicIfNil(err, "Unable to ping sqlite database.")

	registerRoutes()
	http.ListenAndServe(":5000", nil)
}
