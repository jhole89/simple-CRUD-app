package com.jhole89.simpleCrud.models

import com.google.inject.Inject
import play.api.data.Form
import play.api.data.Forms.{mapping, _}
import play.api.db.slick.{DatabaseConfigProvider, HasDatabaseConfigProvider}
import slick.jdbc.H2Profile.api._
import slick.jdbc.JdbcProfile
import slick.lifted.ProvenShape

import scala.concurrent.{ExecutionContext, Future}

sealed trait BaseContact{
  def userName: String
  def firstName: String
  def lastName: String
}

case class Contact(id: Int, userName: String, firstName: String, lastName: String) extends PK with BaseContact
case class ContactData(userName: String, firstName: String, lastName: String) extends BaseContact

object ContactData {

  val form = Form(
    mapping(
      "userName" -> nonEmptyText,
      "firstName" -> text,
      "lastName" -> text,
    )(ContactData.apply)(ContactData.unapply)
  )

}

class ContactTableDef(tag: Tag) extends Table[Contact](tag, "contact") {

  def id: Rep[Int] = column[Int]("id", O.PrimaryKey,O.AutoInc)
  def userName: Rep[String] = column[String]("user_name")
  def firstName: Rep[String] = column[String]("first_name")
  def lastName: Rep[String] = column[String]("last_name")

  override def * : ProvenShape[Contact] = (id, userName, firstName, lastName) <> (Contact.tupled, Contact.unapply)
}

class Contacts @Inject()(
  protected val dbConfigProvider: DatabaseConfigProvider)(
  implicit executionContext: ExecutionContext) extends HasDatabaseConfigProvider[JdbcProfile] {

  val contacts = TableQuery[ContactTableDef]

  def add(contact: Contact): Future[String] =
    dbConfig.db.run(contacts += contact)
      .map(_ => "Contact successfully added")
      .recover { case ex: Exception => ex.getCause.getMessage }

  def delete(id: Int): Future[Int] = dbConfig.db.run(contacts.filter(_.id === id).delete)

  def get(id: Int): Future[Option[Contact]] = dbConfig.db.run(contacts.filter(_.id === id).result.headOption)

  def listAll: Future[Seq[Contact]] = dbConfig.db.run(contacts.result)
  
  
}
