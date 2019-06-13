package com.jhole89.simpleCrud.models

import com.google.inject.Inject
import play.api.data.Form
import play.api.data.Forms.{mapping, _}
import play.api.db.slick.{DatabaseConfigProvider, HasDatabaseConfigProvider}
import slick.jdbc.H2Profile.api._
import slick.jdbc.JdbcProfile
import slick.lifted.{ForeignKeyQuery, ProvenShape}

import scala.concurrent.{ExecutionContext, Future}

sealed trait BaseEmail {
  def email: String
  def contactId: Int
}


case class Email(id: Int, email: String, contactId: Int) extends PK with BaseEmail
case class EmailData(email: String, contactId: Int) extends BaseEmail

object EmailData {

  val form = Form(
    mapping(
      "email" -> text,
      "contactId" -> number
    )(EmailData.apply)(EmailData.unapply)
  )

}

class EmailTableDef(tag: Tag) extends Table[Email](tag, "email") {

  val contacts = TableQuery[ContactTableDef]
  
  def id: Rep[Int] = column[Int]("id", O.PrimaryKey,O.AutoInc)
  def email: Rep[String] = column[String]("email")
  def contactId: Rep[Int] = column[Int]("contactId")

  override def * : ProvenShape[Email] = (id, email, contactId) <> (Email.tupled, Email.unapply)

  def contact: ForeignKeyQuery[ContactTableDef, Contact] = foreignKey("emails_fk_contact_id", contactId, contacts)(_.id)
}

class Emails @Inject()(
  protected val dbConfigProvider: DatabaseConfigProvider)(
  implicit executionContext: ExecutionContext) extends HasDatabaseConfigProvider[JdbcProfile] {

  val emails = TableQuery[EmailTableDef]

  def add(email: Email): Future[String] =
    dbConfig.db.run(emails += email)
      .map(_ => "Email successfully added")
      .recover { case ex: Exception => ex.getCause.getMessage }

  def delete(id: Int): Future[Int] = dbConfig.db.run(emails.filter(_.id === id).delete)

  def get(id: Int): Future[Option[Email]] = dbConfig.db.run(emails.filter(_.id === id).result.headOption)

  def listAll: Future[Seq[Email]] = dbConfig.db.run(emails.result)
}
