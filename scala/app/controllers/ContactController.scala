package controllers

import javax.inject._
import models._
import play.api.data.Form
import play.api.data.Forms._
import play.api.libs.json.Json
import play.api.mvc._

import scala.concurrent.{ExecutionContext, Future}

class ContactController @Inject()(
  repo: ContactRepository,
  controllerComponents: MessagesControllerComponents
)(implicit executionContext: ExecutionContext)
  extends MessagesAbstractController(controllerComponents) {

  val contactForm: Form[ContactData] = Form {
    mapping(
      "userName" -> nonEmptyText,
      "firstName" -> text,
      "lastName" -> text,
    )(ContactData.apply)(ContactData.unapply)
  }

  def index: Action[AnyContent] = Action { implicit request =>
    Ok(views.html.index(contactForm))
  }

  def createContact: Action[AnyContent] = Action.async { implicit request =>
    contactForm.bindFromRequest.fold(
      errorForm => {
        Future.successful(Ok(views.html.index(errorForm)))
      },
      contact => {
        repo.create(contact.userName, contact.firstName, contact.lastName).map{ _ =>
          Redirect(routes.ContactController.index)
            .flashing("success" -> "contact.created")
        }
      }
    )
  }

  def getContacts: Action[AnyContent] = Action.async { implicit request =>
    repo.listAll.map { contact =>
      Ok(Json.toJson(contact))
    }
  }

}
