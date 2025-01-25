register_response = {
    200: {
            'description': 'User register',
            'content': {
                'application/json': {
                    'example': {'message': 'Register'}
                }
            },
        }
}

login_response = {
    200: {
            'description': 'User login',
            'content': {
                'application/json': {
                    'example': {'access_token': 'string', 'type': 'string'}
                }
            },
        },
    404: {
        'description': 'User not found',
        'content': {
            'application/json': {
                'example': {
                    'message': {
                        'status_code': 404,
                        'detail': 'User not found',
                        'headers': None
                    }
                }
            }
        }
    }
}

books_response = {
    200: {
        'description': 'List of books retrieved successfully.',
        'content': {
            'application/json': {
                'example': [
                    {
                        'id': 21,
                        'title': 'Harry Potter',
                        'author_id': 1,
                        'published_year': 2000,
                        'genre': 'Fiction',
                        'created_at': '2025-01-24T23:34:25.624177',
                        'updated_at': '2025-01-24T23:34:25.624177',
                        'author_name': 'Author1'
                    }
                ]
            },
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer', 'description': 'Unique identifier for the book'},
                        'title': {'type': 'string', 'description': 'Title of the book'},
                        'author_id': {'type': 'integer', 'description': 'Unique identifier for the author'},
                        'published_year': {'type': 'integer', 'description': 'Year the book was published'},
                        'genre': {'type': 'string', 'description': 'Genre of the book'},
                        'created_at': {'type': 'string', 'format': 'date-time', 'description': 'Timestamp of creation'},
                        'updated_at': {'type': 'string', 'format': 'date-time', 'description': 'Timestamp of last update'},
                        'author_name': {'type': 'string', 'description': 'Name of the author'}
                    }
                }
            }
        }
    },
    422: {
        'description': 'Validation error for input parameters.',
        'content': {
            'application/json': {
                'example': {
                    'detail': [
                        {
                            'loc': ['query', 'year_from'],
                            'msg': 'value is not a valid integer',
                            'type': 'type_error.integer'
                        }
                    ]
                }
            }
        },
    },
}

add_book_response = {
    200: {
        'description': 'Book successfully added.',
        'content': {
            'application/json': {
                'example': {
                    'id': 1,
                    'title': 'Start Wars',
                    'author_id': 3,
                    'published_year': 2011,
                    'genre': 'Science',
                    'created_at': '2025-01-25T12:00:00',
                    'updated_at': '2025-01-25T12:00:00',
                    'author_name': 'Author1'
                }
            }
        }
    },
    401: {
        'description': 'Unauthorized. Access token is missing or invalid.',
        'content': {
            'application/json': {
                'example': {'detail': 'Unauthorized'}
            }
        }
    },
    422: {
        'description': 'Validation error for input parameters.',
        'content': {
            'application/json': {
                'example': {
                    'detail': [
                        {'loc': ['body', 'title'], 'msg': 'field required', 'type': 'value_error.missing'},
                        {'loc': ['body', 'author_name'], 'msg': 'field required', 'type': 'value_error.missing'}
                    ]
                }
            }
        }
    }
}

book_detail_response = {
    200: {
        'description': 'Book retrieved successfully.',
        'content': {
            'application/json': {
                'example': {
                    'id': 21,
                    'title': 'Harry Potter',
                    'author_id': 1,
                    'published_year': 2000,
                    'genre': 'Fiction',
                    'created_at': '2025-01-24T23:34:25.624177',
                    'updated_at': '2025-01-24T23:34:25.624177',
                    'author_name': 'Author1'
                }
            }
        }
    },
    404: {
        'description': 'Book not found.',
        'content': {
            'application/json': {
                'example': {
                    'detail': 'Book with the given ID was not found.'
                }
            }
        }
    }
}

book_update_responses = {
    200: {
        'description': 'Book updated successfully.',
        'content': {
            'application/json': {
                'example': {
                    'id': 21,
                    'title': 'Updated Book Title',
                    'author_id': 1,
                    'published_year': 2000,
                    'genre': 'Updated Genre',
                    'created_at': '2025-01-24T23:34:25.624177',
                    'updated_at': '2025-01-25T10:00:00.000000',
                    'author_name': 'Updated Author'
                }
            }
        }
    },
    404: {
        'description': 'Book not found.',
        'content': {
            'application/json': {
                'example': {
                    'detail': 'Book with the given ID was not found.'
                }
            }
        }
    },
    401: {
        'description': 'Unauthorized access.',
        'content': {
            'application/json': {
                'example': {
                    'detail': 'Unauthorized'
                }
            }
        }
    }
}

book_delete_responses = {
    200: {
        'description': 'Book deleted successfully.',
        'content': {
            'application/json': {
                'example': {
                    'message': 'Deleted'
                }
            }
        }
    },
    404: {
        'description': 'Book not found.',
        'content': {
            'application/json': {
                'example': {
                    'detail': 'Book not found'
                }
            }
        }
    },
    401: {
        'description': 'Unauthorized access.',
        'content': {
            'application/json': {
                'example': {
                    'detail': 'Unauthorized'
                }
            }
        }
    }
}

books_import_responses = {
    200: {
        'description': 'Books imported successfully.',
        'content': {
            'application/json': {
                'example': {
                    'message': 'Books imported successfully'
                }
            }
        }
    },
    400: {
        'description': 'Invalid file format or error during processing.',
        'content': {
            'application/json': {
                'example': {
                    'detail': 'Unsupported file type. Please upload a JSON file.'
                }
            }
        }
    },
    401: {
        'description': 'Unauthorized access.',
        'content': {
            'application/json': {
                'example': {
                    'detail': 'Unauthorized'
                }
            }
        }
    }
}

