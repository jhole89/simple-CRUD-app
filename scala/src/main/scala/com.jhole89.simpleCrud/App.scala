package com.jhole89.simpleCrud

import com.jhole89.simpleCrud.controllers.ContactController
import com.jhole89.simpleCrud.models.{Contact, ContactData}
import javax.inject._
import play.api.Logging
import play.api.mvc._

import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future

@Singleton
class App @Inject()(cc: ControllerComponents, contactController: ContactController) extends AbstractController(cc) with Logging {

  def index() = Action.async {
    implicit request: Request[AnyContent] =>
      contactController.listAllContacts.map { users => Ok(views.html.index(ContactData.form, users)) }
  }

  def addContact() = Action.async {
    implicit request: Request[AnyContent] =>
      ContactData.form.bindFromRequest.fold(
        errorForm => {
          logger.warn(s"Form submission with error: ${errorForm.errors}")
          Future.successful(Ok(views.html.index(errorForm, Seq.empty[Contact])))
        },
        data => contactController
          .addContact(Contact(0, data.userName, data.firstName, data.lastName))
          .map( _ => Redirect(routes.App.index()))
      )
  }

  def deleteContact(id: Int) = Action.async {
    implicit request: Request[AnyContent] =>
      contactController.deleteContact(id).map { _ =>
        Redirect(routes.App.index())
      }
  }

}