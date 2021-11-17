import requests
from python_helper import Constant as c
from python_helper import ReflectionHelper, ObjectHelper, log, Function, StringHelper

from python_framework.api.src.util import FlaskUtil
from python_framework.api.src.util import Serializer
from python_framework.api.src.domain import HttpDomain
from python_framework.api.src.constant import HttpClientConstant
from python_framework.api.src.converter.static import ConverterStatic
from python_framework.api.src.enumeration.HttpStatus import HttpStatus
from python_framework.api.src.service.flask import FlaskManager
from python_framework.api.src.service.openapi import OpenApiManager
from python_framework.api.src.service.ExceptionHandler import GlobalException


class HttpClientEvent(Exception):
    def __init__(self, verb, *args, **kwargs):
        if ObjectHelper.isNone(verb):
            raise Exception('Http client event verb cannot be none')
        Exception.__init__(self, f'Http client {verb} event')
        self.verb = verb
        self.args = args
        self.kwargs = kwargs


class ManualHttpClientEvent(Exception):
    def __init__(self, completeResponse):
        Exception.__init__(self, f'Manual http client event')
        self.completeResponse = completeResponse


def getHttpClientEvent(resourceInstanceMethod, *args, **kwargs):
    completeResponse = None
    try:
        completeResponse = resourceInstanceMethod(*args, **kwargs)
    except HttpClientEvent as httpClientEvent:
        return httpClientEvent
    except Exception as exception:
        raise exception
    if ObjectHelper.isNotNone(completeResponse):
        return ManualHttpClientEvent(completeResponse)


def raiseHttpClientEventNotFoundException(*args, **kwargs):
    raise Exception('HttpClientEvent not found')


@Function
def HttpClient(url=c.BLANK, headers=None, timeout=HttpClientConstant.DEFAULT_TIMEOUT, logRequest=False, logResponse=False) :
    clientUrl = url
    clientHeaders = ConverterStatic.getValueOrDefault(headers, dict())
    clientTimeout = timeout
    clientLogRequest = logRequest
    clientLogResponse = logResponse
    def Wrapper(OuterClass, *args, **kwargs):
        log.wrapper(HttpClient,f'''wrapping {OuterClass.__name__}''')
        class InnerClass(OuterClass):
            url = clientUrl
            headers = clientHeaders
            timeout = clientTimeout
            logRequest = clientLogRequest
            logResponse = clientLogResponse
            def __init__(self,*args, **kwargs):
                log.wrapper(OuterClass,f'in {InnerClass.__name__}.__init__(*{args},**{kwargs})')
                apiInstance = FlaskManager.getApi()
                OuterClass.__init__(self,*args, **kwargs)
                self.globals = apiInstance.globals
            def options(self, *args, **kwargs):
                raise HttpClientEvent(HttpDomain.Verb.OPTIONS, *args, **kwargs)
            def get(self, *args, **kwargs):
                raise HttpClientEvent(HttpDomain.Verb.GET, *args, **kwargs)
            def post(self, *args, **kwargs):
                raise HttpClientEvent(HttpDomain.Verb.POST, *args, **kwargs)
            def put(self, *args, **kwargs):
                raise HttpClientEvent(HttpDomain.Verb.PUT, *args, **kwargs)
            def patch(self, *args, **kwargs):
                raise HttpClientEvent(HttpDomain.Verb.PATCH, *args, **kwargs)
            def delete(self, *args, **kwargs):
                raise HttpClientEvent(HttpDomain.Verb.DELETE, *args, **kwargs)
        ReflectionHelper.overrideSignatures(InnerClass, OuterClass)
        return InnerClass
    return Wrapper


class ClientMethodConfig:
    def __init__(self,
        url = None,
        headers = None,
        requestHeaderClass = None,
        requestParamClass = None,
        requestClass = None,
        responseClass = None,
        returnOnlyBody = None,
        timeout = None,
        propagateAuthorization = None,
        propagateApiKey = None,
        propagateSession = None,
        produces = None,
        consumes = None,
        logRequest = None,
        logResponse = None
    ):
        self.url = url
        self.headers = headers
        self.requestHeaderClass = requestHeaderClass
        self.requestParamClass = requestParamClass
        self.requestClass = requestClass
        self.responseClass = responseClass
        self.returnOnlyBody = returnOnlyBody
        self.timeout = timeout
        self.propagateAuthorization = propagateAuthorization
        self.propagateApiKey = propagateApiKey
        self.propagateSession = propagateSession
        self.produces = produces
        self.consumes = consumes
        self.logRequest = logRequest
        self.logResponse = logResponse


@Function
def HttpClientMethod(
    url = c.BLANK,
    headers = None,
    requestHeaderClass = None,
    requestParamClass = None,
    requestClass = None,
    responseClass = None,
    returnOnlyBody = True,
    timeout = None,
    propagateAuthorization = False,
    propagateApiKey = False,
    propagateSession = False,
    consumes = OpenApiManager.DEFAULT_CONTENT_TYPE,
    produces = OpenApiManager.DEFAULT_CONTENT_TYPE,
    logRequest = False,
    logResponse = False
):
    clientMethodConfig = ClientMethodConfig(
        url = url,
        headers = headers,
        requestHeaderClass = requestHeaderClass,
        requestParamClass = requestParamClass,
        requestClass = requestClass,
        responseClass = responseClass,
        returnOnlyBody = returnOnlyBody,
        timeout = timeout,
        propagateAuthorization = propagateAuthorization,
        propagateApiKey = propagateApiKey,
        propagateSession = propagateSession,
        produces = produces,
        consumes = consumes,
        logRequest = logRequest,
        logResponse = logResponse,
    )
    def innerMethodWrapper(resourceInstanceMethod,*args, **kwargs) :

        def options(
            resourceInstance,
            body = None,
            additionalUrl = None,
            params = None,
            headers = None,
            timeout = None,
            logRequest = False,
            **kwargs
        ):
            verb = HttpDomain.Verb.OPTIONS
            url, params, headers, body, timeout, logRequest = parseParameters(
                resourceInstance,
                clientMethodConfig,
                additionalUrl,
                params,
                headers,
                body,
                timeout,
                logRequest
            )
            doLogRequest(verb, url, body, params, headers, logRequest)
            clientResponse = requests.options(
                url,
                params = params,
                headers = headers,
                json = body,
                timeout = timeout,
                **kwargs
            )
            return clientResponse

        def get(
            resourceInstance,
            body = None,
            additionalUrl = None,
            params = None,
            headers = None,
            timeout = None,
            logRequest = False,
            **kwargs
        ):
            verb = HttpDomain.Verb.GET
            url, params, headers, body, timeout, logRequest = parseParameters(
                resourceInstance,
                clientMethodConfig,
                additionalUrl,
                params,
                headers,
                body,
                timeout,
                logRequest
            )
            doLogRequest(verb, url, body, params, headers, logRequest)
            clientResponse = requests.get(
                url,
                params = params,
                headers = headers,
                json = body,
                timeout = timeout,
                **kwargs
            )
            return clientResponse

        def post(
            resourceInstance,
            body = None,
            additionalUrl = None,
            headers = None,
            params = None,
            timeout = None,
            logRequest = False,
            **kwargs
        ):
            verb = HttpDomain.Verb.POST
            url, params, headers, body, timeout, logRequest = parseParameters(
                resourceInstance,
                clientMethodConfig,
                additionalUrl,
                params,
                headers,
                body,
                timeout,
                logRequest
            )
            doLogRequest(verb, url, body, params, headers, logRequest)
            clientResponse = requests.post(
                url,
                params = params,
                headers = headers,
                json = body,
                timeout = timeout,
                **kwargs
            )
            return clientResponse

        def put(
            resourceInstance,
            body = None,
            additionalUrl = None,
            headers = None,
            params = None,
            timeout = None,
            logRequest = False,
            **kwargs
        ):
            verb = HttpDomain.Verb.PUT
            url, params, headers, body, timeout, logRequest = parseParameters(
                resourceInstance,
                clientMethodConfig,
                additionalUrl,
                params,
                headers,
                body,
                timeout,
                logRequest
            )
            doLogRequest(verb, url, body, params, headers, logRequest)
            clientResponse = requests.put(
                url,
                params = params,
                headers = headers,
                json = body,
                timeout = timeout,
                **kwargs
            )
            return clientResponse

        def patch(
            resourceInstance,
            body = None,
            additionalUrl = None,
            headers = None,
            params = None,
            timeout = None,
            logRequest = False,
            **kwargs
        ):
            verb = HttpDomain.Verb.PATCH
            url, params, headers, body, timeout, logRequest = parseParameters(
                resourceInstance,
                clientMethodConfig,
                additionalUrl,
                params,
                headers,
                body,
                timeout,
                logRequest
            )
            doLogRequest(verb, url, body, params, headers, logRequest)
            clientResponse = requests.patch(
                url,
                params = params,
                headers = headers,
                json = body,
                timeout = timeout,
                **kwargs
            )
            return clientResponse

        def delete(
            resourceInstance,
            body = None,
            additionalUrl = None,
            headers = None,
            params = None,
            timeout = None,
            logRequest = False,
            **kwargs
        ):
            verb = HttpDomain.Verb.DELETE
            url, params, headers, body, timeout, logRequest = parseParameters(
                resourceInstance,
                clientMethodConfig,
                additionalUrl,
                params,
                headers,
                body,
                timeout,
                logRequest
            )
            doLogRequest(verb, url, body, params, headers, logRequest)
            clientResponse = requests.delete(
                url,
                params = params,
                headers = headers,
                json = body,
                timeout = timeout,
                **kwargs
            )
            return clientResponse

        def doLogRequest(verb, url, body, params, headers, logRequest):
            log.info(resourceInstanceMethod, f'Client {verb} - {url}')
            if logRequest:
                log.prettyJson(
                    resourceInstanceMethod,
                    'Request',
                    {
                        'headers': ConverterStatic.getValueOrDefault(headers, dict()),
                        'query': ConverterStatic.getValueOrDefault(params, dict()),
                        'body': ConverterStatic.getValueOrDefault(body, dict())
                    },
                    condition = True,
                    logLevel = log.INFO
                )

        HTTP_CLIENT_RESOLVERS_MAP = {
            HttpDomain.Verb.OPTIONS : options,
            HttpDomain.Verb.GET : get,
            HttpDomain.Verb.POST : post,
            HttpDomain.Verb.PUT : put,
            HttpDomain.Verb.PATCH : patch,
            HttpDomain.Verb.DELETE : delete
        }

        log.wrapper(HttpClientMethod,f'''wrapping {resourceInstanceMethod.__name__}''')
        def innerResourceInstanceMethod(*args, **kwargs):
            f'''(*args, {FlaskUtil.KW_HEADERS}={{}}, {FlaskUtil.KW_PARAMETERS}={{}}, **kwargs)'''
            resourceInstance = args[0]
            clientResponse = None
            completeResponse = None
            try :
                FlaskManager.validateKwargs(
                    kwargs,
                    resourceInstance,
                    resourceInstanceMethod,
                    requestHeaderClass,
                    requestParamClass
                )
                FlaskManager.validateArgs(args, requestClass, resourceInstanceMethod)
                clientResponse = None
                httpClientEvent = getHttpClientEvent(resourceInstanceMethod, *args, **kwargs)
                if isinstance(httpClientEvent, ManualHttpClientEvent):
                    completeResponse = httpClientEvent.completeResponse
                elif isinstance(httpClientEvent, HttpClientEvent):
                    try :
                        clientResponse = HTTP_CLIENT_RESOLVERS_MAP.get(
                            httpClientEvent.verb,
                            raiseHttpClientEventNotFoundException
                        )(
                            resourceInstance,
                            *httpClientEvent.args,
                            **httpClientEvent.kwargs
                        )
                    except Exception as exception:
                        raiseException(clientResponse, exception)
                    raiseExceptionIfNeeded(clientResponse)
                    completeResponse = getCompleteResponse(clientResponse, responseClass, produces)
                    FlaskManager.validateCompleteResponse(responseClass, completeResponse)
                else:
                    raise Exception('Unknown http client event')
            except Exception as exception:
                log.log(innerResourceInstanceMethod, 'Failure at client method execution', exception=exception, muteStackTrace=True)
                FlaskManager.raiseAndPersistGlobalException(exception, resourceInstance, resourceInstanceMethod, context=HttpDomain.CLIENT_CONTEXT)
            clientResponseStatus = completeResponse[-1]
            clientResponseHeaders = completeResponse[1]
            clientResponseBody = completeResponse[0] if ObjectHelper.isNotNone(completeResponse[0]) else {'message' : HttpStatus.map(clientResponseStatus).enumName}
            if resourceInstance.logResponse or logResponse :
                log.prettyJson(
                    resourceInstanceMethod,
                    'Response',
                    {
                        'headers': clientResponseHeaders,
                        'body': Serializer.getObjectAsDictionary(clientResponseBody),
                        'status': clientResponseStatus
                    },
                    condition = True,
                    logLevel = log.INFO
                )
            if returnOnlyBody:
                return completeResponse[0]
            else:
                return completeResponse
        ReflectionHelper.overrideSignatures(innerResourceInstanceMethod, resourceInstanceMethod)
        innerResourceInstanceMethod.url = clientMethodConfig.url
        innerResourceInstanceMethod.headers = clientMethodConfig.headers
        innerResourceInstanceMethod.requestHeaderClass = clientMethodConfig.requestHeaderClass
        innerResourceInstanceMethod.requestParamClass = clientMethodConfig.requestParamClass
        innerResourceInstanceMethod.requestClass = clientMethodConfig.requestClass
        innerResourceInstanceMethod.responseClass = clientMethodConfig.responseClass
        innerResourceInstanceMethod.returnOnlyBody = clientMethodConfig.returnOnlyBody
        innerResourceInstanceMethod.timeout = clientMethodConfig.timeout
        innerResourceInstanceMethod.propagateAuthorization = clientMethodConfig.propagateAuthorization
        innerResourceInstanceMethod.propagateApiKey = clientMethodConfig.propagateApiKey
        innerResourceInstanceMethod.propagateSession = clientMethodConfig.propagateSession
        innerResourceInstanceMethod.produces = clientMethodConfig.produces
        innerResourceInstanceMethod.consumes = clientMethodConfig.consumes
        innerResourceInstanceMethod.logRequest = clientMethodConfig.logRequest
        innerResourceInstanceMethod.logResponse = clientMethodConfig.logResponse

        return innerResourceInstanceMethod
    return innerMethodWrapper


@Function
def getUrl(client, clientMethodConfig, additionalUrl):
    return StringHelper.join(
        [
            ConverterStatic.getValueOrDefault(u, c.BLANK) for u in [
                client.url,
                clientMethodConfig.url,
                additionalUrl
            ]
        ],
        character = c.BLANK
    )


@Function
def getHeaders(client, clientMethodConfig, headers):
    return {
        **ConverterStatic.getValueOrDefault(client.headers, dict()),
        **{HttpDomain.HeaderKey.CONTENT_TYPE: clientMethodConfig.consumes},
        **ConverterStatic.getValueOrDefault(clientMethodConfig.headers, dict()),
        **ConverterStatic.getValueOrDefault(headers, dict())
    }


@Function
def getTimeout(client, clientMethodConfig, timeout):
    return ConverterStatic.getValueOrDefault(timeout, ConverterStatic.getValueOrDefault(clientMethodConfig.timeout, client.timeout))


@Function
def getLogRequest(client, clientMethodConfig, logRequest):
    return client.logRequest or clientMethodConfig.logRequest or logRequest


@Function
def parseParameters(client, clientMethodConfig, additionalUrl, params, headers, body, timeout, logRequest):
    url = getUrl(client, clientMethodConfig, additionalUrl)
    params = ConverterStatic.getValueOrDefault(params, dict())
    headers = getHeaders(client, clientMethodConfig, headers)
    body = ConverterStatic.getValueOrDefault(body, dict())
    timeout = getTimeout(client, clientMethodConfig, timeout)
    logRequest = getLogRequest(client, clientMethodConfig, logRequest)
    return url, params, headers, body, timeout, logRequest


def raiseException(clientResponse, exception):
    raise GlobalException(
        logMessage = getErrorMessage(clientResponse, exception=exception),
        url = FlaskUtil.safellyGetRequestUrlFromResponse(clientResponse),
        status = FlaskUtil.safellyGetResponseStatus(clientResponse),
        logHeaders = {
            'requestHeaders': FlaskUtil.safellyGetRequestHeadersFromResponse(clientResponse),
            'responseHeaders': FlaskUtil.safellyGetResponseHeaders(clientResponse)
        },
        logPayload = {
            'requestBody': FlaskUtil.safellyGetRequestJsonFromResponse(clientResponse),
            'responseBody': FlaskUtil.safellyGetResponseJson(clientResponse)
        },
        context = HttpDomain.CLIENT_CONTEXT
    )


def raiseExceptionIfNeeded(clientResponse):
    status = FlaskUtil.safellyGetResponseStatus(clientResponse) ###- clientResponse.status_code
    if ObjectHelper.isNone(status) or 500 <= status:
        raise GlobalException(
            logMessage = getErrorMessage(clientResponse),
            url = FlaskUtil.safellyGetRequestUrlFromResponse(clientResponse),
            status = status,
            logHeaders = {
                'requestHeaders': FlaskUtil.safellyGetRequestHeadersFromResponse(clientResponse),
                'responseHeaders': FlaskUtil.safellyGetResponseHeaders(clientResponse)
            },
            logPayload = {
                'requestBody': FlaskUtil.safellyGetRequestJsonFromResponse(clientResponse),
                'responseBody': FlaskUtil.safellyGetResponseJson(clientResponse)
            },
            context = HttpDomain.CLIENT_CONTEXT
        )
    elif 400 <= status:
        raise GlobalException(
            message = getErrorMessage(clientResponse),
            logMessage = HttpClientConstant.ERROR_AT_CLIENT_CALL_MESSAGE,
            url = FlaskUtil.safellyGetRequestUrlFromResponse(clientResponse),
            status = status,
            logHeaders = {
                'requestHeaders': FlaskUtil.safellyGetRequestHeadersFromResponse(clientResponse),
                'responseHeaders': FlaskUtil.safellyGetResponseHeaders(clientResponse)
            },
            logPayload = {
                'requestBody': FlaskUtil.safellyGetRequestJsonFromResponse(clientResponse),
                'responseBody': FlaskUtil.safellyGetResponseJson(clientResponse)
            },
            context = HttpDomain.CLIENT_CONTEXT
        )


@Function
def getCompleteResponse(clientResponse, responseClass, produces, fallbackStatus=HttpStatus.INTERNAL_SERVER_ERROR):
    responseBody, responseHeaders, responseStatus = dict(), dict(), fallbackStatus
    responseHeaders = FlaskUtil.safellyGetResponseHeaders(clientResponse)
    responseBody = FlaskUtil.safellyGetResponseJson(clientResponse)
    try :
        responseStatus = HttpStatus.map(HttpStatus.NOT_FOUND if ObjectHelper.isNone(clientResponse.status_code) else clientResponse.status_code)
    except Exception as exception :
        responseStatus = HttpStatus.map(fallbackStatus)
        log.warning(getCompleteResponse, f'Not possible to get client response status. Returning {responseStatus} by default', exception=exception)
    responseHeaders = {
        **{HttpDomain.HeaderKey.CONTENT_TYPE: produces},
        **responseHeaders
    }
    responseStatus = ConverterStatic.getValueOrDefault(responseStatus, HttpStatus.map(fallbackStatus))
    if ObjectHelper.isNone(responseClass):
        return responseBody, responseHeaders, responseStatus
    return Serializer.convertFromJsonToObject(responseBody, responseClass), responseHeaders, responseStatus


@Function
def getErrorMessage(clientResponse, exception=None):
    completeErrorMessage = f'{HttpClientConstant.ERROR_AT_CLIENT_CALL_MESSAGE}{c.DOT_SPACE}{HttpClientConstant.CLIENT_DID_NOT_SENT_ANY_MESSAGE}'
    errorMessage = HttpClientConstant.CLIENT_DID_NOT_SENT_ANY_MESSAGE
    possibleErrorMessage = None
    bodyAsJson = {}
    try :
        bodyAsJson = clientResponse.json()
    except Exception as innerException :
        bodyAsJsonException = FlaskUtil.safellyGetResponseJson(clientResponse)
        log.log(getErrorMessage, f'Invalid client response: {bodyAsJsonException}', exception=innerException)
        log.debug(getErrorMessage, f'Not possible to get error message from client response: {bodyAsJsonException}. Proceeding with value {bodyAsJson} by default', exception=innerException, muteStackTrace=True)
    try:
        if ObjectHelper.isNotNone(clientResponse):
            if ObjectHelper.isDictionary(bodyAsJson):
                possibleErrorMessage = bodyAsJson.get('message', bodyAsJson.get('error')).strip()
            if ObjectHelper.isList(bodyAsJson) and 0 < len(bodyAsJson):
                possibleErrorMessage = bodyAsJson[0].get('message', bodyAsJson[0].get('error')).strip()
        if ObjectHelper.isNotNone(possibleErrorMessage) and StringHelper.isNotBlank(possibleErrorMessage):
            errorMessage = f'{c.LOG_CAUSE}{possibleErrorMessage}'
        else:
            log.debug(getErrorMessage, f'Client response {FlaskUtil.safellyGetResponseJson(clientResponse)}')
        exceptionPortion = HttpClientConstant.ERROR_AT_CLIENT_CALL_MESSAGE if ObjectHelper.isNone(exception) or StringHelper.isBlank(exception) else str(exception)
        completeErrorMessage = f'{exceptionPortion}{c.DOT_SPACE}{errorMessage}'
    except Exception as exception:
        log.warning(getErrorMessage, f'Not possible to get error message. Returning {completeErrorMessage} by default', exception=exception)
    return completeErrorMessage
