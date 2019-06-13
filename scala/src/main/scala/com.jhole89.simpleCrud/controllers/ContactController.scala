package com.jhole89.simpleCrud.controllers

import com.google.inject.Inject
import com.jhole89.simpleCrud.models.{Contact, Contacts}

import scala.concurrent.Future

class ContactController @Inject()(contacts: Contacts) {

  def addContact(contact: Contact): Future[String] = contacts.add(contact)

  def deleteContact(id: Int): Future[Int] = contacts.delete(id)

  def getContact(id: Int): Future[Option[Contact]] = contacts.get(id)

  def listAllContacts: Future[Seq[Contact]] = contacts.listAll

}
