package models

import javax.inject.{Inject, Singleton}
import play.api.db.slick.{DatabaseConfigProvider, HasDatabaseConfigProvider}
import play.api.libs.json._
import slick.jdbc.JdbcProfile
import slick.lifted.ProvenShape

import scala.concurrent.{ExecutionContext, Future}

sealed trait BaseContact{
  def userName: String
  def firstName: String
  def lastName: String
}

case class ContactData(userName: String, firstName: String, lastName: String) extends BaseContact
case class Contact(id: Int, userName: String, firstName: String, lastName: String) extends PK with BaseContact

object Contact {
  implicit val contactFormat = Json.format[Contact]
}

@Singleton
class ContactRepository @Inject()(
  protected val dbConfigProvider: DatabaseConfigProvider
)(implicit executionContext: ExecutionContext)
  extends HasDatabaseConfigProvider[JdbcProfile] {

  import profile.api._

  private class ContactTableDef(tag: Tag) extends Table[Contact](tag, "contacts") {

    def id: Rep[Int] = column[Int]("id", O.PrimaryKey,O.AutoInc)
    def userName: Rep[String] = column[String]("user_name")
    def firstName: Rep[String] = column[String]("first_name")
    def lastName: Rep[String] = column[String]("last_name")

    override def * : ProvenShape[Contact] = (id, userName, firstName, lastName) <> ((Contact.apply _).tupled, Contact.unapply)
  }

  private val contacts = TableQuery[ContactTableDef]

  def create(userName: String, firstName: String, lastName: String): Future[Contact] = db.run {
    (contacts
      .map(c => (c.userName, c.firstName, c.lastName))
      returning contacts.map(_.id)
      into ((details, id) => Contact(id, details._1, details._2, details._3))
    ) += (userName, firstName, lastName)
  }

  def get(id: Int): Future[Option[Contact]] = db.run{
    contacts.filter(_.id === id).result.headOption
  }

  def listAll: Future[Seq[Contact]] = db.run{
    contacts.result
  }

  def delete(id: Int): Future[Int] = db.run {
    contacts.filter(_.id === id).delete
  }




}
