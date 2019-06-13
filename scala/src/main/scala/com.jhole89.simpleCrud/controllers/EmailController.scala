package com.jhole89.simpleCrud.controllers

import com.google.inject.Inject
import com.jhole89.simpleCrud.models.{Email, Emails}

import scala.concurrent.Future

class EmailController @Inject()(emails: Emails) {

  def addCEmail(email: Email): Future[String] = emails.add(email)

  def deleteEmail(id: Int): Future[Int] = emails.delete(id)

  def getEmail(id: Int): Future[Option[Email]] = emails.get(id)

  def listAllEmails: Future[Seq[Email]] = emails.listAll

}
